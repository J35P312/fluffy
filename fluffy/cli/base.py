"""Fluffy base command"""

import logging
import pathlib
import shutil

import click
import coloredlogs

from fluffy.cli.make_analysis import analyse
from fluffy.cli.make_reference import reference
from fluffy.cli.make_rerun import rerun
from fluffy.config import get_configs
from fluffy.samplesheet import read_samplesheet
from fluffy.slurm_api import SlurmAPI
from fluffy.version import __version__

LOG = logging.getLogger(__name__)
LOG_LEVELS = ["DEBUG", "INFO", "WARNING"]


@click.group()
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(LOG_LEVELS),
    help="Choose what log messages to show",
)
@click.option(
    "--config",
    "-c",
    required=True,
    type=click.Path(exists=True),
    help="json config file",
)
@click.version_option(__version__)
@click.option("--out", "-o", required=True, help="output folder")
@click.option(
    "--sample",
    "-s",
    type=click.Path(exists=True),
    required=True,
    help="path to samplesheet",
)
@click.option(
    "--project",
    "-p",
    type=click.Path(exists=True),
    required=True,
    help="input project folder",
)
@click.pass_context
def base_command(ctx, log_level, config, out, sample, project):
    """Fluffy base command"""
    coloredlogs.install(log_level)
    ctx.obj = {}

    out = pathlib.Path(out)
    LOG.info("Create outdir %s (if not exist)", out)
    out.mkdir(parents=True, exist_ok=True)

    config = pathlib.Path(config)
    configs = get_configs(config)
    configs["out"] = out
    configs["name"]=config.name
    configs["config_path"]=config
    ctx.obj["configs"] = configs

    new_config = out / config.name

    project_dir = pathlib.Path(project)
    ctx.obj["project"] = project_dir
    configs["project"] = project_dir

    sacct_dir = out / "sacct"
    sacct_dir.mkdir(parents=True, exist_ok=True)

    with open(sample, "r") as samplesheet:
        ctx.obj["samples"] = list(read_samplesheet(samplesheet, project_dir))

    ctx.obj["sample_sheet"] = sample

    ctx.obj["slurm_api"] = SlurmAPI(
        slurm_settings=configs["slurm"], out_dir=out,
    )


base_command.add_command(reference)
base_command.add_command(rerun)
base_command.add_command(analyse)
