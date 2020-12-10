"""Commands that use the WisecondorX package"""

from pathlib import Path


def get_convert_cmd(singularity_exe: str, out_prefix: str) -> str:
    """Get command for converting bam to called nipt"""
    cmd = (
        f"singularity exec {singularity_exe} WisecondorX convert {out_prefix}.bam "
        f"{out_prefix}.bam.wcx.npz"
    )
    return cmd


def get_newref_cmd(singularity_exe: str, out: str, binsize: str) -> str:
    """Get command for creating reference bam to called nipt"""
    cmd = (
        f"singularity exec {singularity_exe} WisecondorX newref {out}/**/*.wcx.npz "
        f"{out.rstrip('/')}.wcxref.{binsize}.npz --nipt --binsize {binsize}"
    )
    return cmd


def get_mkref_cmd(
    singularity_exe: str, out: str, testbinsize: str, prefacebinsize: str
) -> str:
    """Command to generate wisecondorX reference files"""
    wcx_mkref = get_newref_cmd(singularity_exe, out, testbinsize)

    wcx_mkrefpreface = get_newref_cmd(singularity_exe, out, prefacebinsize)

    return "\n".join([wcx_mkref, wcx_mkrefpreface])


def get_predict_cmd(
    singularity_exe: str,
    out_prefix: Path,
    reference: str,
    blacklist: str,
    zscore: str,
    preface: bool = False,
):
    """Get a string with command for running the wisecondor X test"""
    out = out_prefix.with_suffix(".WCXpredict")
    if preface:
        out = out_prefix.with_suffix(".WCXpredict" + ".preface")

    predict_cmd = (
        f"singularity exec {singularity_exe} WisecondorX --loglevel info predict "
        f"{str(out_prefix)}.bam.wcx.npz {reference} {str(out)} --bed --blacklist "
        f"{blacklist} --zscore {zscore}"
    )

    return predict_cmd


def get_gender_cmd(singularity_exe: str, out_prefix: str, reference: str):
    """Get a string with command for running the wisecondor X test"""
    gender_cmd = (
        f"singularity exec {singularity_exe} WisecondorX gender {out_prefix}.bam.wcx.npz "
        f"{reference} > {out_prefix}.wcx.npz.gender.txt"
    )

    return gender_cmd
