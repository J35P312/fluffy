"""Cli command to make a reference"""

import logging

import click

from fluffy.config import check_configs
from fluffy.workflows.wisecondor import make_reference

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--dry-run", is_flag=True, help="Do not create any files")
@click.pass_context
def reference(ctx, dry_run):
    """Create a reference for """
    LOG.info("Running fluffy reference")
    configs = ctx.obj["configs"]
    try:
        # Not sure where to include skip preface...
        check_configs(configs, mkref=True)
    except FileNotFoundError as err:
        raise click.Abort
    configs = ctx.obj["configs"]
    slurm_api = ctx.obj["slurm_api"]

    jobid = make_reference(
        samples=ctx.obj["samples"],
        configs=configs,
        slurm_api=slurm_api,
        dry_run=dry_run,
    )
    LOG.info("Running make reference on slurm with jobid %s", jobid)
