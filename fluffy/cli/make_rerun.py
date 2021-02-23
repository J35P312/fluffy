"""CLI to rerun failed samples"""
import logging

import click

from fluffy.config import check_configs
from fluffy.deliverables import print_deliverables
from fluffy.status import print_status, check_status
from fluffy.workflows.analyse_samples import analyse_workflow
import shutil
import os

LOG = logging.getLogger(__name__)


@click.command()
@click.pass_context
@click.option(
    "--skip-preface", is_flag=True, help="Skip preface fetal fraction estimation"
)
@click.option("--dry-run", is_flag=True, help="Do not create any files")
def rerun(ctx, skip_preface, dry_run):
    """Run the pipeline to call NIPT"""
    LOG.info("Running fluffy rerun")
    samples = ctx.obj["samples"]
    configs = ctx.obj["configs"]
    configs["sample_sheet"] = ctx.obj["sample_sheet"]
    project_dir=ctx.obj["project"]
    slurm_api = ctx.obj["slurm_api"]

    config_path=configs["out"] / configs["name"]
    try:
        check_configs(configs, skip_preface=skip_preface)
    except FileNotFoundError as err:
        raise click.Abort
    output_dir=configs["out"]

    analysis_status = check_status(
        output_dir=output_dir
    )

    if analysis_status:
       run_version=analysis_status["fluffy_version"]
       analysis_time=analysis_status["analysis_time"]

    else:
       print("Error analysis status file is missing!")

    failed_samples=set([])

    first=True
    complete=True
    if analysis_status:
        for line in open(f"{output_dir}/sacct/fluffy_{analysis_time}.log.status"):
            content=line.strip().split()
            if first:
               first=False
               continue

            if not "COMPLETED" in content[-2]:
               complete=False

            if not "summarizebatch-" in line and not "COMPLETED" == content[-2] and not "fluffy-complete" in line:
          
               sample_id="-".join(content[1].split("-")[1:-1])
               print(f"FAIL:{content[1]}")
               failed_samples.add(sample_id)        

    if not analysis_status:
        pass       
    elif not analysis_status["analysis_run_status"] =="fail":
        print("Error: analysis status is not fail")
        print("make sure that the analysis is failed, and edit the analysis_run_status.json file")
        quit()

    if complete and analysis_status:
        print("Error: no failed jobs detected")
        print("make sure that the analysis is failed, or rerun it using the analysis module")
        quit()


    print_status(
        output_dir=output_dir,
    )

    for sample in failed_samples:
        if sample == "":
           continue

        try:
           shutil.rmtree(f"{output_dir}/{sample}")
        except:
           pass

        try:
           os.remove(f"{output_dir}/{sample}.fluffy-{run_version}.zip")
        except:
           pass

    if os.path.exists(f"{output_dir}/FAIL"):
        os.remove(f"{output_dir}/FAIL")

    if os.path.exists(f"{output_dir}/summary.csv"):
        os.remove(f"{output_dir}/summary.csv")

    if os.path.exists(f"{output_dir}/multiqc_report.html"):
        os.remove(f"{output_dir}/multiqc_report.html")

    try:
        shutil.rmtree(f"{output_dir}/multiqc_data")
    except:
        pass

    ok_samples=[]
    for sample in samples:
        if sample["sample_id"] in failed_samples:
            ok_samples.append(sample)

    analyse_workflow(
        samples=ok_samples,
        configs=configs,
        skip_preface=skip_preface,
        slurm_api=slurm_api,
        dry_run=dry_run,
    )
