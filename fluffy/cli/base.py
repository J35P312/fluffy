"""Fluffy base command"""

import logging
import pathlib
import shutil

import click
import coloredlogs

from fluffy.config import check_configs, get_configs
from fluffy.samplesheet import read_samplesheet
from fluffy.version import __version__
from fluffy.workflows.make_model import make_call_model
from fluffy.workflows.make_ref import make_reference

LOG = logging.getLogger(__name__)
LOG_LEVELS = ["DEBUG", "INFO", "WARNING"]


@click.command()
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

    ctx["samples"] = read_samplesheet(pathlib.Path(sample), project_dir)


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

    if config["preface"]["model_dir"] == "":
        LOG.error("the model_dir parameter is not set, check your config file")
        raise click.Abort

    make_call_model(samples=ctx.obj["samples"], out_dir=ctx.obj["out"], configs=configs)


@click.command()
def analyse():
    """Run the pipeline to call NIPT"""
    jobids = []
    for sample in samples:
        os.system("mkdir {}/{}".format(args.out, sample))

        fastq = samples[sample]
        if fastq["se"]:
            run_bwa = align_and_convert_single_end(
                config, fastq["fastq"][0], args, sample
            )
        else:
            run_bwa = align_and_convert_paired_end(config, fastq["fastq"], args, sample)

        bwa = Slurm(
            "bwaAln-{}".format(sample),
            {
                "account": config["slurm"]["account"],
                "partition": "node",
                "time": config["slurm"]["time"],
            },
            log_dir="{}/logs".format(args.out),
            scripts_dir="{}/scripts".format(args.out),
        )
        align_jobid = bwa.run(run_bwa)

        run_ffy = amycne_ffy(config, args, sample)
        ffy = Slurm(
            "amycne-{}".format(sample),
            {
                "account": config["slurm"]["account"],
                "partition": "core",
                "time": config["slurm"]["time"],
            },
            log_dir="{}/logs".format(args.out),
            scripts_dir="{}/scripts".format(args.out),
        )
        jobids.append(ffy.run(run_ffy, depends_on=[align_jobid]))

        run_picard = picard_qc(config, args, sample)
        picard = Slurm(
            "picard_qc-{}".format(sample),
            {
                "account": config["slurm"]["account"],
                "partition": "core",
                "time": config["slurm"]["time"],
            },
            log_dir="{}/logs".format(args.out),
            scripts_dir="{}/scripts".format(args.out),
        )
        jobids.append(picard.run(run_picard, depends_on=[align_jobid]))

        run_wcx = wisecondorx_test(config, args, sample)
        wcx_test = Slurm(
            "wcx-{}".format(sample),
            {
                "account": config["slurm"]["account"],
                "partition": "core",
                "time": config["slurm"]["time"],
            },
            log_dir="{}/logs".format(args.out),
            scripts_dir="{}/scripts".format(args.out),
        )
        jobids.append(wcx_test.run(run_wcx, depends_on=[align_jobid]))
        wcx_test_jobid = jobids[-1]

        if not args.skip_preface:
            run_preface = preface(config, args, sample)
            preface_predict = Slurm(
                "preface_predict-{}".format(sample),
                {
                    "account": config["slurm"]["account"],
                    "partition": "core",
                    "time": config["slurm"]["time"],
                },
                log_dir="{}/logs".format(args.out),
                scripts_dir="{}/scripts".format(args.out),
            )
            jobids.append(preface_predict.run(run_preface, depends_on=[wcx_test_jobid]))

    run_summarise = summarise(config, args)
    summarise_batch = Slurm(
        "summarise_batch-{}".format(args.project.strip("/").split("/")[-1]),
        {
            "account": config["slurm"]["account"],
            "partition": "core",
            "time": config["slurm"]["time"],
        },
        log_dir="{}/logs".format(args.out),
        scripts_dir="{}/scripts".format(args.out),
    )
    summarise_batch.run(run_summarise, depends_on=jobids)
