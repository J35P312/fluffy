"""Fluffy base command"""

import logging
import pathlib
import shutil
import argparse
import sys
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

def base_arguments(args_list):
    parser = argparse.ArgumentParser("""Fluffy-{}""".format(__version__),add_help=False)
    parser.add_argument("--reference", help="call structural variation", action="store_true")
    parser.add_argument("--analyse"   , help="Run the fluffy analysis", action="store_true")
    parser.add_argument("--rerun"     , help="rerun failed analyses", action="store_true")
    parser.add_argument("--version"     , help="Print version", required=False, action="store_true")
    args, unknown = parser.parse_known_args(args_list)

    if not args.reference and not args.analyse and not args.rerun and not args.version:
        parser.print_help()
        quit()

    if args.version:
        return(args)

    parser.add_argument("-c",'--config'	  , type=str, help="json config file", required=True)
    parser.add_argument("-o",'--out'	  , type=str, help="output folder", required=True)
    parser.add_argument("-p",'--project'	  , type=str, help="input fastq", required=True)
    parser.add_argument("-s",'--sample'	  , type=str, help="path to samplesheet", required=True)
    parser.add_argument("-l",'--slurm_params'	  ,nargs='+', type=str, help="Additional parameters passed to slurm on the following format QoS:High  ")
    parser.add_argument("--dry_run"     , help="dry run, do not generate output files", required=False, action="store_true")
    args, unknown = parser.parse_known_args(args_list)

    return(args,parser)

def base_command():
    args,parser=base_arguments(sys.argv[1:])

    if args.version:
       print("Fluffy-{}".format(__version__))
       quit()

    coloredlogs.install("INFO")
    ctx= {}

    sample=args.sample
    out=pathlib.Path(args.out)
    LOG.info("Create outdir %s (if not exist)", out)

    out.mkdir(parents=True, exist_ok=True)
    config = pathlib.Path(args.config)
    configs = get_configs(config)
    configs["out"] = out
    configs["name"]=config.name
    configs["config_path"]=config
    ctx["configs"] = configs

    new_config = out / config.name

    project_dir = pathlib.Path(args.project)
    ctx["project"] = project_dir
    configs["project"] = project_dir

    sacct_dir = out / "sacct"
    sacct_dir.mkdir(parents=True, exist_ok=True)

    with open(sample, "r") as samplesheet:
        ctx["samples"] = list(read_samplesheet(samplesheet, project_dir))

    ctx["sample_sheet"] = sample
    if args.slurm_params:
        for param in args.slurm_params:
            configs["slurm"][ param.split(":")[0] ]=param.split(":")[-1]

    ctx["slurm_api"] = SlurmAPI(
        slurm_settings=configs["slurm"], out_dir=out,
    )

    if args.reference:
        reference(args,ctx, args.dry_run)

    elif args.rerun:
        parser.add_argument("--batch-ref"     , help="Build a wisecondorX refeference from the input batch (overrides refpreface and reftest)", required=False, action="store_true")
        parser.add_argument("--skip-preface"     , help="Skip preface fetal fraction estimation", required=False, action="store_true")
        args, unknown = parser.parse_known_args()

        rerun(args,ctx,args.skip_preface, args.dry_run)

    elif args.analyse:
        parser.add_argument("--batch-ref"     , help="Build a wisecondorX refeference from the input batch (overrides refpreface and reftest)", required=False, action="store_true")
        parser.add_argument("--skip-preface"     , help="Skip preface fetal fraction estimation", required=False, action="store_true")
        args, unknown = parser.parse_known_args()

        analyse(ctx,args.skip_preface,args.dry_run,args.batch_ref)

    else:
        parser.print_help()
