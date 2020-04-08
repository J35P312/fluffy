"""Workflows for the preface program"""

import logging
from pathlib import Path
from typing import Iterator

from slurmpy import Slurm

from fluffy.commands.preface import (get_preface_model_cmd,
                                     get_preface_predict_cmd)
from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)


def get_output_lines(samples: Iterator[dict], out_dir: Path) -> list:
    """Create a config file for preface based wisecondor x and AMYCNE data"""
    out = []
    for sample in samples:
        sample_id = sample["sample_id"]
        in_file = out_dir / sample_id / ".".join([sample_id, "AMYCNE.tab"])
        if not in_file.exists():
            LOG.info("Could not find file %s", in_file)
            continue

        for line in open(in_file, "r"):
            if "medA" in line:
                continue
            content = line.strip().split()
            if "female" in line:
                fetal_fraction = "NA"
                gender = "F"
            else:
                gender = "M"
                fetal_fraction = float(content[-2]) * 100

            file_path = (
                out_dir
                / sample_id
                / ".".join([sample_id, "WCXpredict.preface_bins.bed"])
            )
            file_path_str = str(file_path.absolute())

            out.append(f"{sample_id}\t{file_path_str}\t{gender}\t{fetal_fraction}")
    return out


def make_call_model(samples: Iterator[dict], out_dir: Path, configs: dict):
    """create a call model"""

    out_lines = get_output_lines(samples, out_dir)
    config_path = out_dir / "PREFACE.config.tab"
    with open(config_path, "w") as out_file:
        out_file.write("ID\tfilepath\tgender\tFF\n")
        out_file.write("\n".join(out_lines))

    # Something is wrong here, should this command run for each sample?
    # Should it be sent to slurm?
    model_cmd = get_preface_model_cmd(
        singularity_exe=configs["singularity"],
        config_path=config_path,
        model_dir=configs["preface"]["model_dir"],
        settings=configs["preface"]["modelsettings"],
    )

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    preface_model = Slurm(
        "preface_model",
        {
            "account": configs["slurm"]["account"],
            "partition": "core",
            "time": configs["slurm"]["time"],
        },
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )

    jobid = preface_model.run(model_cmd)

    return jobid


def preface_predict_workflow(
    configs: dict,
    sample_id: str,
    dependency: int,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
):
    """Run the preface predict workflow"""
    LOG.info("Running the preface predict workflow")
    out_dir = configs["out"]

    preface_predict_cmd = get_preface_predict_cmd(
        singularity_exe=configs["singularity"],
        out_dir=out_dir,
        model_dir=configs["preface"]["model_dir"],
        sample_id=sample_id,
    )

    jobid = slurm_api.run_job(
        name=f"preface_predict-{sample_id}",
        command=preface_predict_cmd,
        dependencies=[dependency],
        dry_run=dry_run,
    )

    return jobid
