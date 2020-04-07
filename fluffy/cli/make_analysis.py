"""CLI to run the analysis"""
import logging

import click

from fluffy.config import check_configs
from fluffy.workflows.analyse_samples import analyse_workflow

LOG = logging.getLogger(__name__)


@click.command()
@click.pass_context
@click.option(
    "--skip-preface", is_flag=True, help="Skip preface fetal fraction estimation"
)
@click.option("--dry-run", is_flag=True, help="Do not create any files")
def analyse(ctx, skip_preface, dry_run):
    """Run the pipeline to call NIPT"""
    LOG.info("Running fluffy analyse")
    samples = ctx["samples"]
    out_dir = ctx["out"]
    configs = ctx.obj["configs"]

    try:
        check_configs(configs, skip_preface=skip_preface)
    except FileNotFoundError as err:
        raise click.Abort

    analyse_workflow(
        samples=list(samples),
        out_dir=out_dir,
        configs=configs,
        skip_preface=skip_preface,
        dry_run=dry_run,
    )
