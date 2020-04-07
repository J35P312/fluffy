"""CLI for making a preface model"""
import logging

import click

from fluffy.config import check_configs
from fluffy.workflows.preface import make_call_model

LOG = logging.getLogger(__name__)


@click.command()
@click.pass_context
def model(ctx):
    """Create a model for """
    LOG.info("Running fluffy model")
    configs = ctx.obj["configs"]
    try:
        # Not sure where to include skip preface...
        check_configs(configs)
    except FileNotFoundError as err:
        raise click.Abort

    if configs["preface"]["model_dir"] == "":
        LOG.error("the model_dir parameter is not set, check your config file")
        raise click.Abort

    make_call_model(samples=ctx.obj["samples"], out_dir=ctx.obj["out"], configs=configs)
