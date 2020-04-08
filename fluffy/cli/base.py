"""Fluffy base command"""

import logging
import pathlib
import shutil

import click
import coloredlogs

from fluffy.cli.make_analysis import analyse
from fluffy.cli.make_model import model
from fluffy.cli.make_reference import reference
from fluffy.config import get_configs
from fluffy.samplesheet import read_samplesheet
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
    ctx["out"] = out
    LOG.info("Create outdir %s (if not exist)", out)
    out.mkdir(parents=True, exist_ok=True)

    config = pathlib.Path(config)
    ctx["configs"] = get_configs(config)

    new_config = out / config.name
    if new_config.exists():
        LOG.warning("Config already exists, create new dir or remove config")
        raise click.Abort

    LOG.info("Copy config to %s", new_config)
    shutil.copy(config, str(new_config))

    project_dir = pathlib.Path(project)
    ctx["project"] = project_dir

    with open(sample, "r") as samplesheet:
        ctx["samples"] = read_samplesheet(samplesheet, project_dir)

    ctx["sample_sheet"] = sample


base_command.add_command(reference)
base_command.add_command(model)
base_command.add_command(analyse)
