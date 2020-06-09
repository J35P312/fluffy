"""CLI to run the analysis"""
import logging

import click

from fluffy.config import check_configs
from fluffy.deliverables import print_deliverables
from fluffy.status import print_status
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
    samples = ctx.obj["samples"]
    configs = ctx.obj["configs"]
    configs["sample_sheet"] = ctx.obj["sample_sheet"]
    project_dir=ctx.obj["project"]
    slurm_api = ctx.obj["slurm_api"]

    try:
        check_configs(configs, skip_preface=skip_preface)
    except FileNotFoundError as err:
        raise click.Abort

    print_deliverables(
        output_dir=configs["out"],
        project_dir=project_dir,
        samples=samples,
    )

    print_status(
        output_dir=configs["out"],
    )

    analyse_workflow(
        samples=list(samples),
        configs=configs,
        skip_preface=skip_preface,
        slurm_api=slurm_api,
        dry_run=dry_run,
    )
