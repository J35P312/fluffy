"""Worklflows to run wisecondor"""

from typing import Iterator

from fluffy.commands.pipelines import wisecondor_x_test
from fluffy.commands.wisecondor import get_mkref_cmd
from fluffy.slurm_api import SlurmAPI
from fluffy.workflows.align import align_individual


def make_reference(
    samples: Iterator[dict], configs: dict, slurm_api: SlurmAPI, dry_run: bool = None
) -> int:
    """Create a reference based on some samples"""
    out_dir = configs["out"]
    jobids = []
    for sample in samples:
        align_jobid = align_individual(
            configs=configs, sample=sample, slurm_api=slurm_api, dry_run=dry_run
        )
        jobids.append(align_jobid)

    mkref_cmd = get_mkref_cmd(
        singularity_exe=configs["singularity"],
        out=str(out_dir),
        testbinsize=configs["wisecondorx"]["testbinsize"],
        prefacebinsize=configs["wisecondorx"]["prefacebinsize"],
    )

    jobid = slurm_api.run_job(
        name="wcxmkref", command=mkref_cmd, dependencies=jobids, dry_run=dry_run,
    )

    return jobid


def wisecondor_xtest_workflow(
    configs: dict,
    sample_id: str,
    dependency: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
):
    """Run the wisecondor x test workflow"""
    out_dir = configs["out"]
    run_wcx_pipe = wisecondor_x_test(
        configs=configs, out_dir=out_dir, sample_id=sample_id
    )

    jobid = slurm_api.run_job(
        name=f"wcx-{sample_id}",
        command=run_wcx_pipe,
        dependencies=[dependency],
        dry_run=dry_run,
    )

    return jobid
