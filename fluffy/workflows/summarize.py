"""Summarize the analysis"""

import logging
import os
import sys

from pathlib import Path

from fluffy.slurm_api import SlurmAPI
from fluffy.commands.multiqc import get_multiqc_cmd
from fluffy.singularity_cmd import singularity_base

LOG = logging.getLogger(__name__)


def get_summarize_cmd(
    singularity: str, out_dir: Path,project_id: str, sample_sheet: str, zscore: str, mincnv: str
) -> str:
    """Return a string with the command to summarize a run"""

    outfile = out_dir / f"{project_id}.csv"
    wd=os.path.dirname(os.path.realpath(__file__)).replace("fluffy/workflows","scripts")

    summary_cmd = (
        f"python {wd}/generate_csv.py "
        f"--folder {str(out_dir)} --samplesheet {sample_sheet} --Zscore {zscore} --minCNV {mincnv} "
        f"> {str(outfile)}"
    )
    return summary_cmd

def get_two_pass_ref_cmd(
    singularity: str,
    out_dir: Path,
    project_id: str,
    working_directory: str, 
    preface_bin_size: int,
    wisecondor_bin_size: int,
    ) -> str:

    outfile = out_dir / f"{project_id}.1pass.csv"

    two_bass_ref_cmd = (
        f"python {working_directory}/filter_csv.py --csv {outfile} --project {out_dir} --singularity \"{singularity}\" --binsize {preface_bin_size} {wisecondor_bin_size}"
    )
    
    return(two_bass_ref_cmd)

def summarize_workflow(
    configs: dict, afterok: list, slurm_api: SlurmAPI, dry_run: bool = False,two_pass: bool = False, 
) -> int:
    """Run the workflow to summarize an analysis"""
    LOG.info("Run the summarize workflow")
    out_dir = configs["out"]

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    wd=os.path.dirname(os.path.realpath(__file__)).replace("fluffy/workflows","scripts")

    if not two_pass:

        summarize_cmd = get_summarize_cmd(
            singularity=singularity,
            out_dir=out_dir,
            project_id=configs["project_id"],
            sample_sheet=configs["sample_sheet"],
            zscore=configs["summary"]["zscore"],
            mincnv=configs["summary"]["mincnv"],
        )


        multiqc_cmd=get_multiqc_cmd(singularity=singularity,input_dir=out_dir,out_dir=out_dir)

        command_str=f"{multiqc_cmd}\n{summarize_cmd}"
    else:
        summarize_cmd = get_summarize_cmd(
           singularity=singularity,
           out_dir=out_dir,
           project_id=configs["project_id"]+".1pass",
           sample_sheet=configs["sample_sheet"],
           zscore=configs["summary"]["zscore"],
           mincnv=configs["summary"]["mincnv"],
        )

        build_two_pass_ref=get_two_pass_ref_cmd(singularity,out_dir,configs["project_id"],wd,configs["wisecondorx"]["testbinsize"],configs["wisecondorx"]["prefacebinsize"])
        command_str=f"{summarize_cmd}\n{build_two_pass_ref}"


    jobid = slurm_api.run_job(
        name=f"summarize_batch",
        command=command_str,
        afterok=afterok,
        dry_run=dry_run,
    )

    return jobid
