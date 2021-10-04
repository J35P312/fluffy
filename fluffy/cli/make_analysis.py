"""CLI to run the analysis"""
import logging

import shutil

from fluffy.config import check_configs
from fluffy.deliverables import print_deliverables
from fluffy.status import print_status
from fluffy.workflows.analyse_samples import analyse_workflow


LOG = logging.getLogger(__name__)

def analyse(ctx, skip_preface, dry_run ,batch_ref):
    """Run the pipeline to call NIPT"""
    LOG.info("Running fluffy analyse")

    samples = ctx["samples"]
    configs = ctx["configs"]
    configs["sample_sheet"] = ctx["sample_sheet"]	
    project_dir=ctx["project"]
    slurm_api = ctx["slurm_api"]

    config_path=configs["out"] / configs["name"]
    if config_path.exists():
        LOG.warning("Config already exists, create new dir or remove config")
        quit()


    LOG.info("Copy config to %s", config_path)
    shutil.copy(configs["config_path"], str(config_path))
    try:
        check_configs(configs, skip_preface=skip_preface)
    except FileNotFoundError as err:
        print("config not found")
        quit()

    summarise_prefix="summary"
    project_ids=set([])
    for sample in samples:
         if "project" in sample:
             project_ids.add(sample["project"])
         else:
             continue

    if len(project_ids) == 1:
         summarise_prefix=list(project_ids)[0]

    print_deliverables(
        output_dir=configs["out"],
        batch_ref=batch_ref,
        project_dir=project_dir,
        project_id=summarise_prefix,
        samples=samples,
    )

    print_status(
        output_dir=configs["out"],
    )

    configs["project_id"]=summarise_prefix
    analyse_workflow(
        samples=list(samples),
        configs=configs,
        skip_preface=skip_preface,
        slurm_api=slurm_api,
        dry_run=dry_run,
        batch_ref=batch_ref,
    )
