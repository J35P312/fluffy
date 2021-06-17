"""Commands that use the WisecondorX package"""

from pathlib import Path


def get_convert_cmd(singularity: str, out_prefix: str) -> str:
    """Get command for converting bam to called nipt"""
    cmd = (
        f"{singularity} WisecondorX convert {out_prefix}.bam "
        f"{out_prefix}.bam.wcx.npz"
    )
    return cmd


def get_newref_cmd(singularity: str, out: str, binsize: str) -> str:
    """Get command for creating reference npz"""
    cmd = (
        f"n=0\n"
        f"until [ \"$n\" -ge 5 ]\n"
        f"do\n"
        f"{singularity} WisecondorX newref {out}/**/*.wcx.npz "
        f"{out.rstrip('/')}.wcxref.{binsize}.npz --nipt --binsize {binsize} && break\n"
        f"n=$((n+1))\n"
        f"sleep 10\n"
        f"done"
    )
    return cmd


def get_mkref_cmd(
    singularity: str, out: str, testbinsize: str, prefacebinsize: str
) -> str:
    """Command to generate wisecondorX reference files"""
    wcx_mkref = get_newref_cmd(singularity, out, testbinsize)

    wcx_mkrefpreface = get_newref_cmd(singularity, out, prefacebinsize)

    return "\n".join([wcx_mkref, wcx_mkrefpreface])


def get_predict_cmd(
    singularity: str,
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
        f"{singularity} WisecondorX --loglevel info predict "
        f"{str(out_prefix)}.bam.wcx.npz {reference} {str(out)} --bed --blacklist "
        f"{blacklist} --zscore {zscore}"
    )

    return predict_cmd


def get_gender_cmd(singularity: str, out_prefix: str, reference: str):
    """Get a string with command for running the wisecondor X test"""
    gender_cmd = (
        f"{singularity} WisecondorX gender {out_prefix}.bam.wcx.npz "
        f"{reference} > {out_prefix}.wcx.npz.gender.txt"
    )

    return gender_cmd
