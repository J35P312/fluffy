"""Cli command to make a reference"""

import logging

import click
import shutil 

from fluffy.config import check_configs
from fluffy.workflows.wisecondor import make_reference
from fluffy.status import print_status

LOG = logging.getLogger(__name__)


@click.command()
@click.option("--dry-run", is_flag=True, help="Do not create any files")
@click.pass_context
def reference(ctx, dry_run):
    """Create a reference for WisecondorX"""
    LOG.info("Running fluffy reference")
    configs = ctx.obj["configs"]
    try:
        check_configs(configs, mkref=True)
    except FileNotFoundError as err:
        raise click.Abort

    configs = ctx.obj["configs"]
    slurm_api = ctx.obj["slurm_api"]

    config_path=configs["out"] / configs["name"]
    if config_path.exists():
        LOG.warning("Config already exists, create new dir or remove config")
        raise click.Abort

    LOG.info("Copy config to %s", config_path)
    shutil.copy(configs["config_path"], str(config_path))


    print_status(
        output_dir=configs["out"],
    )

    jobid = make_reference(
        samples=ctx.obj["samples"],
        configs=configs,
        slurm_api=slurm_api,
        dry_run=dry_run,
    )
    LOG.info("Running make reference on slurm with jobid %s", jobid)
