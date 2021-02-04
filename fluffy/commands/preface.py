"""Code to get commands for running the preface program"""

from pathlib import Path

from .utils import get_outprefix


def get_preface_predict_cmd(
    singularity: str, out_dir: Path, model_dir: str, sample_id: str
) -> str:
    """Create command for doing fetal fraction estimation using Preface"""
    out_prefix = get_outprefix(out_dir, sample_id)
    predict_cmd = (
        f"{singularity} Rscript /bin/PREFACE-0.1.1/PREFACE.R predict --infile"
        f" {str(out_prefix)}.WCXpredict.preface_bins.bed --model {model_dir}/model.RData > "
        f"{str(out_prefix)}_bins.bed.PREFACE.txt"
    )

    return predict_cmd


def get_preface_model_cmd(
    singularity: str, config_path: Path, model_dir: str, settings: str,
) -> str:
    """Create command for doing fetal fraction estimation using Preface"""
    model_cmd = (
        f"{singularity} Rscript /bin/PREFACE-0.1.1/PREFACE.R train --config "
        f"{str(config_path)} --outdir {model_dir} {settings}"
    )

    return model_cmd
