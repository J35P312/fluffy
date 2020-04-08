"""Workflows to run AMYCNE"""

from fluffy.commands.pipelines import amycne_ffy
from fluffy.slurm_api import SlurmAPI


def estimate_ffy(
    configs: dict,
    sample_id: str,
    dependency: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
) -> int:
    """Run the estimate fetal fraction with AMYCNE"""
    out_dir = configs["out"]
    fetal_fraction_pipe = amycne_ffy(
        configs=configs, out_dir=out_dir, sample_id=sample_id
    )

    job_name = f"amycne-{sample_id}"

    job_id = slurm_api.run_job(
        name=job_name,
        command=fetal_fraction_pipe,
        dependencies=[dependency],
        dry_run=dry_run,
    )

    return job_id
