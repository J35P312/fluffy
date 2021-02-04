"""Workflows for the preface program"""

import logging
from pathlib import Path
from typing import Iterator

from slurmpy import Slurm
from fluffy.singularity_cmd import singularity_base
from fluffy.commands.preface import (get_preface_model_cmd,
                                     get_preface_predict_cmd)
from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)

def preface_predict_workflow(
    configs: dict,
    sample_id: str,
    afterok: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
):
    """Run the preface predict workflow"""
    LOG.info("Running the preface predict workflow")
    out_dir = configs["out"]

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    preface_predict_cmd = get_preface_predict_cmd(
        singularity=singularity,
        out_dir=out_dir,
        model_dir=configs["preface"]["model_dir"],
        sample_id=sample_id,
    )

    jobid = slurm_api.run_job(
        name=f"preface_predict-{sample_id}",
        command=preface_predict_cmd,
        afterok=[afterok],
        dry_run=dry_run,
    )

    return jobid
