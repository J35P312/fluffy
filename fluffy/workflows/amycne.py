"""Workflows to run AMYCNE"""

import pathlib

from slurmpy import Slurm

from fluffy.commands.pipelines import amycne_ffy


def estimate_ffy(
    configs: dict, out_dir: pathlib.Path, sample_id: str, align_jobid: int
) -> int:
    """Run the estimate fetal fraction with AMYCNE"""
    fetal_fraction_pipe = amycne_ffy(
        configs=configs, out_dir=out_dir, sample_id=sample_id
    )

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    fetal_fraction_batch = Slurm(
        f"amycne-{sample_id}",
        {
            "account": configs["slurm"]["account"],
            "partition": "core",
            "time": configs["slurm"]["time"],
        },
        log_dir=log_dir,
        scripts_dir=scripts_dir,
    )

    job_id = fetal_fraction_batch.run(fetal_fraction_pipe, depends_on=[align_jobid])
    return job_id
