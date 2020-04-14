"""Workflow for analysing all samples in a batch"""

from typing import Iterator

from fluffy.slurm_api import SlurmAPI
from fluffy.workflows.align import align_individual
from fluffy.workflows.amycne import estimate_ffy
from fluffy.workflows.cleanup import cleanup_workflow
from fluffy.workflows.picard import picard_qc_workflow
from fluffy.workflows.preface import preface_predict_workflow
from fluffy.workflows.summarize import summarize_workflow
from fluffy.workflows.wisecondor import wisecondor_xtest_workflow


def analyse_workflow(
    samples: Iterator[dict],
    configs: dict,
    slurm_api: SlurmAPI,
    skip_preface: bool = False,
    dry_run: bool = False,
) -> int:
    """Run the wisecondor chromosome x analysis"""
    jobids = []
    for sample in samples:
        sample_jobids = []
        sample_id = sample["sample_id"]
        sample_outdir = configs["out"] / sample_id
        # This will fail if dir already exists
        sample_outdir.mkdir(parents=True)

        align_jobid = align_individual(
            configs=configs, sample=sample, slurm_api=slurm_api, dry_run=dry_run,
        )

        ffy_jobid = estimate_ffy(
            configs=configs,
            sample_id=sample_id,
            dependency=align_jobid,
            slurm_api=slurm_api,
            dry_run=dry_run,
        )
        jobids.append(ffy_jobid)
        sample_jobids.append(ffy_jobid)

        picard_jobid = picard_qc_workflow(
            configs=configs,
            sample_id=sample_id,
            dependency=align_jobid,
            slurm_api=slurm_api,
            dry_run=dry_run,
        )
        jobids.append(picard_jobid)
        sample_jobids.append(picard_jobid)

        wcx_test_jobid = wisecondor_xtest_workflow(
            configs=configs,
            sample_id=sample_id,
            dependency=align_jobid,
            slurm_api=slurm_api,
            dry_run=dry_run,
        )

        jobids.append(wcx_test_jobid)
        sample_jobids.append(wcx_test_jobid)

        if not skip_preface:
            preface_predict_jobid = preface_predict_workflow(
                configs=configs,
                sample_id=sample_id,
                dependency=wcx_test_jobid,
                slurm_api=slurm_api,
                dry_run=dry_run,
            )
            jobids.append(preface_predict_jobid)
            sample_jobids.append(preface_predict_jobid)

        cleanup_workflow(
            configs=configs,
            sample_outdir=sample_outdir,
            sample_id=sample_id,
            dependencies=sample_jobids,
            slurm_api=slurm_api,
            dry_run=dry_run,
        )

    summarize_jobid = summarize_workflow(
        configs=configs, dependencies=jobids, slurm_api=slurm_api, dry_run=dry_run
    )
    return summarize_jobid
