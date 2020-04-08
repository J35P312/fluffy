"""Cli command to make a reference"""

import logging

import click

from fluffy.config import check_configs
from fluffy.workflows.wisecondor import make_reference

LOG = logging.getLogger(__name__)


@click.command()
@click.pass_context
def reference(ctx):
    """Create a reference for """
    LOG.info("Running fluffy reference")
    configs = ctx.obj["configs"]
    try:
        # Not sure where to include skip preface...
        check_configs(configs, mkref=True)
    except FileNotFoundError as err:
        raise click.Abort

    jobid = make_reference(
        samples=ctx.obj["samples"], out_dir=ctx.obj["out"], configs=configs
    )
    LOG.info("Running make reference on slurm with jobid %s", jobid)
