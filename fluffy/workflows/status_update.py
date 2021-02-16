"""Workflows to update the fluffy analysis run status"""

import logging

from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)

def sed_replace_inplace(
    in_filename: str,project_dir:str ,flag: str, find_str: str, replace_str: str
) -> str:
    """create a command for running sed find and replace inplace"""
    cmd = (
        f"sed -i \'s/{find_str}/{replace_str}/g\' {in_filename}\n"
        f"echo {replace_str} > {project_dir}/{flag}"
    )
    return cmd

def pipe_complete(
    configs: dict,
    afterok: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
) -> int:
    """Run Sed to update the analysis run flag"""
    out_dir = configs["out"]

    sed_replace_inplace_cmd = sed_replace_inplace(
        in_filename= str(out_dir / "analysis_status.json"),project_dir=str(out_dir),flag="COMPLETE", find_str=" \"running\"", replace_str=" \"complete\""
    )

    jobid = slurm_api.run_job(
        name="fluffy-complete",
        command=sed_replace_inplace_cmd,
        afterok=[afterok],
        dry_run=dry_run,
    )

    return jobid

def pipe_fail(
    configs: dict,
    slurm_api: SlurmAPI,
    afternotok: int,
    dry_run: bool = False,
) -> int:
    """Run Sed to update the analysis run flag"""
    out_dir = configs["out"]

    sed_replace_inplace_cmd = sed_replace_inplace(
        in_filename= str(out_dir / "analysis_status.json"),project_dir=str(out_dir),flag="FAIL", find_str=" \"running\"", replace_str=" \"fail\""
    )

    jobid = slurm_api.run_job(
        name="fluffy-fail",
        command=sed_replace_inplace_cmd,
        afternotok=[afternotok],
        dry_run=dry_run,
    )

    return jobid
