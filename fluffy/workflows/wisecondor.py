"""Worklflows to run wisecondor"""

from typing import Iterator

from fluffy.commands.pipelines import wisecondor_x_test
from fluffy.commands.wisecondor import get_mkref_cmd
from fluffy.singularity_cmd import singularity_base
from fluffy.slurm_api import SlurmAPI
from fluffy.workflows.align import align_individual
from fluffy.workflows.status_update import pipe_complete
from fluffy.workflows.status_update import pipe_fail


def make_reference(
    samples: Iterator[dict], configs: dict, slurm_api: SlurmAPI, dry_run: bool = None
) -> int:
    """Create a reference based on some samples"""
    out_dir = configs["out"]
    jobids = []
    for sample in samples:
        

        sample_id = sample["sample_id"]
        sample_outdir = configs["out"] / sample_id

        # This will fail if dir already exists
        sample_outdir.mkdir(parents=True)

        slurm_api.slurm_settings["ntasks"]=configs["align"]["ntasks"]
        slurm_api.slurm_settings["mem"]=configs["align"]["mem"]

        align_jobid = align_individual(
            configs=configs, sample=sample, slurm_api=slurm_api, dry_run=dry_run
        )
        jobids.append(align_jobid)

        slurm_api.slurm_settings["ntasks"]=configs["slurm"]["ntasks"]
        slurm_api.slurm_settings["mem"]=configs["slurm"]["mem"]

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    mkref_cmd = get_mkref_cmd(
        singularity=singularity,
        out=str(out_dir),
        testbinsize=configs["wisecondorx"]["testbinsize"],
        prefacebinsize=configs["wisecondorx"]["prefacebinsize"],
    )

    jobid = slurm_api.run_job(
        name="wcxmkref", command=mkref_cmd, afterok=jobids, dry_run=dry_run,
    )

    slurm_api.slurm_settings["time"]="1:00:00"
    pipe_complete(
        configs=configs, afterok=jobid, slurm_api=slurm_api, dry_run=dry_run
    )
    pipe_fail(
	configs=configs, slurm_api=slurm_api, dry_run=dry_run, afternotok=jobid
    )



    return jobid


def wisecondor_xtest_workflow(
    configs: dict,
    sample_id: str,
    afterok: int,
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
        afterok=[afterok],
        dry_run=dry_run,
    )

    return jobid
