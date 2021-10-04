"""Cli command to make a reference"""

import logging

import shutil 

from fluffy.config import check_configs
from fluffy.workflows.wisecondor import make_reference
from fluffy.status import print_status

LOG = logging.getLogger(__name__)


def reference(args,ctx, dry_run):
    """Create a reference for WisecondorX"""
    LOG.info("Running fluffy reference")

    configs = ctx["configs"]
    try:
        check_configs(configs, mkref=True)
    except FileNotFoundError as err:
        raise click.Abort

    configs = ctx["configs"]
    slurm_api = ctx["slurm_api"]

    config_path=configs["out"] / configs["name"]
    if config_path.exists():
        LOG.warning("Config already exists, create new dir or remove config")
        quit()

    LOG.info("Copy config to %s", config_path)
    shutil.copy(configs["config_path"], str(config_path))

    print_status(
        output_dir=configs["out"],
    )

    jobid = make_reference(
        samples=ctx["samples"],
        configs=configs,
        slurm_api=slurm_api,
        dry_run=dry_run,
    )

    LOG.info("Running make reference on slurm with jobid %s", jobid)
