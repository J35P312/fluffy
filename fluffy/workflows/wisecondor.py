"""Worklflows to run wisecondor"""

from pathlib import Path
from typing import Iterator

from slurmpy import Slurm

from fluffy.commands.pipelines import wisecondor_x_test
from fluffy.commands.wisecondor import get_mkref_cmd
from fluffy.workflows.align import align_individual


def make_reference(
    samples: Iterator[dict], out_dir: Path, configs: dict, dry_run: bool = None
) -> int:
    """Create a reference based on some samples"""
    jobids = []
    for sample in samples:
        align_jobid = align_individual(
            configs=configs, sample=sample, out_dir=out_dir, dry_run=dry_run
        )
        jobids.append(align_jobid)

    mkref_cmd = get_mkref_cmd(
        singularity_exe=configs["singularity"],
        out=out_dir,
        testbinsize=configs["wisecondorx"]["testbinsize"],
        prefacebinsize=configs["wisecondorx"]["prefacebinsize"],
    )

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    make_reference_batch = Slurm(
        "wcxmkref",
        {
            "account": configs["slurm"]["account"],
            "partition": "node",
            "time": configs["slurm"]["time"],
        },
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )

    job_id = make_reference_batch.run(mkref_cmd, depends_on=jobids)

    return job_id


def wisecondor_xtest_workflow(
    configs: dict, out_dir: Path, sample_id: str, align_jobid: int
):
    """Run the wisecondor x test workflow"""
    run_wcx = wisecondor_x_test(configs=configs, out_dir=out_dir, sample_id=sample_id)

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    wcx_test = Slurm(
        "wcx-{}".format(sample_id),
        {
            "account": configs["slurm"]["account"],
            "partition": "core",
            "time": configs["slurm"]["time"],
        },
        log_dir=log_dir,
        scripts_dir=scripts_dir,
    )
    jobid = wcx_test.run(run_wcx, depends_on=[align_jobid])

    return jobid
