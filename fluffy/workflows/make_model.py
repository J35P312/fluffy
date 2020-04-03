"""Code for making a model"""

import logging
import pathlib
from typing import Iterator

from fluffy.commands.preface import get_preface_cmd

LOG = logging.getLogger(__name__)


def get_output_lines(samples: Iterator[dict], out_dir: pathlib.Path) -> list:
    """docstring for get_output_lines"""
    out = []
    for sample in samples:
        sample_id = sample["sample_id"]
        in_file = out_dir / sample_id / ".".join([sample_id, "AMYCNE.tab"])
        if not in_file.exists():
            LOG.info("Could not find file %s", in_file)
            continue
        for line in open(in_file):
            if "medA" in line:
                continue
            content = line.strip().split()
            if "female" in line:
                # What is this?
                ff = "NA"
                gender = "F"
            else:
                gender = "M"
                ff = float(content[-2]) * 100

            file_path = (
                out_dir
                / sample_id
                / ".".join([sample_id, "WCXpredict.preface_bins.bed"])
            )
            out.append(f"{sample_id}\t{file_path}\t{gender}\t{ff}")
    return out


def make_call_model(samples: Iterator[dict], out_dir: pathlib.Path, configs: dict):
    """create a call model"""

    out_lines = get_output_lines(samples, out_dir)
    with open("{}.PREFACE.config.tab".format(out_dir), "w") as out_file:
        out_file.write("ID\tfilepath\tgender\tFF\n")
        out_file.write("\n".join(out_lines))

    # Something is wrong here, should this command run for each sample?
    # Should it be sent to slurm?
    model = get_preface_cmd(
        singularity_exe=configs["singularity"],
        out_dir=out_dir,
        model_dir=configs["preface"]["model_dir"],
        sample_id=sample_id,
    )
