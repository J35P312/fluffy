"""Code for preface command"""

import pathlib

from .utils import get_outprefix


def get_preface_cmd(
    singularity_exe: str, out_dir: pathlib.Path, model_dir: str, sample_id: str
) -> str:
    """Create command for doing fetal fraction estimation using Preface"""
    out_prefix = get_outprefix(out_dir, sample_id)
    preface = (
        f"singularity exec {singularity_exe} Rscript /bin/PREFACE-0.1.1/PREFACE.R predict --infile"
        f" {str(out_prefix)}.WCXpredict.preface_bins.bed --model {model_dir}/model.RData > "
        f"{str(out_prefix)}_bins.bed.PREFACE.txt"
    )
    return preface
