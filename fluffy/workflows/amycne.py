"""Workflows to run AMYCNE"""

import logging

from fluffy.commands.pipelines import amycne_ffy
from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)


def estimate_ffy(
    configs: dict,
    sample_id: str,
    afterok: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
) -> int:
    """Run the estimate fetal fraction with AMYCNE"""
    LOG.info("Running the estimate fetal fraction with AMYCNE workflow")
    out_dir = configs["out"]
    fetal_fraction_pipe = amycne_ffy(
        configs=configs, out_dir=out_dir, sample_id=sample_id
    )

    jobid = slurm_api.run_job(
        name=f"amycne-{sample_id}",
        command=fetal_fraction_pipe,
        afterok=[afterok],
        dry_run=dry_run,
    )

    return jobid
