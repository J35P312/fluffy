"""Code for making a model"""

import logging
import pathlib
from typing import Generator

from fluffy.commands.preface import get_preface_command

LOG = logging.getLogger(__name__)


def make_call_model(samples: Generator[dict], out_dir: pathlib.Path, configs: dict):
    """docstring for make_"""

    with open("{}.PREFACE.config.tab".format(out_dir)), "w") as out_file:
        out_file.write("ID\tfilepath\tgender\tFF\n")
        for sample in samples:
            sample_id = sample["sample_id"]
            in_file = out_dir / sample_id / '.'.join([sample_id, "AMYCNE.tab"])
            if not in_file.exists():
                LOG.info("Could not find file %s", in_file)
                continue
            for line in open(in_file):
                if "medA" in line:
                    continue
                content = line.strip().split()
                if "female" in line:
                    ff = "NA"
                    gender = "F"
                else:
                    gender = "M"
                    ff = float(content[-2]) * 100

                out.append(
                    "{}\t{}/{}/{}.WCXpredict.preface_bins.bed\t{}\t".format(
                        sample, str(out_dir), sample_id, sample_id, gender, ff
                    )
                )

        f.write("\n".join(out))

    run_model = get_preface_command(singularity_exe=config["singularity"], out_dir=out_dir, model_dir=config["preface"]["model_dir"], sample_id: strconfig, args, sample)
