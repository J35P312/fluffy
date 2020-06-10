"""Workflows to run picard"""
import logging

from fluffy.commands.pipelines import picard_qc
from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)


def picard_qc_workflow(
    configs: dict,
    sample_id: str,
    afterok: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
):
    """Run the picard pipeline"""
    LOG.info("Running the picard tools QC workflow")
    out_dir = configs["out"]
    picard_qc_pipe = picard_qc(configs=configs, out_dir=out_dir, sample_id=sample_id)

    jobid = slurm_api.run_job(
        name=f"picard_qc-{sample_id}",
        command=picard_qc_pipe,
        afterok=[afterok],
        dry_run=dry_run,
    )

    return jobid
