"""Commands that use the WisecondorX package"""


def get_convert_cmd(singularity_exe: str, out_prefix: str) -> str:
    """Get command for converting bam to called nipt"""
    cmd = (
        f"singularity exec {singularity_exe} WisecondorX convert {out_prefix}.bam "
        f"{out_prefix}.bam.wcx.npz"
    )
    return cmd


def get_newref_cmd(singularity_exe: str, out: str, binsize: str) -> str:
    """Get command for converting bam to called nipt"""
    cmd = (
        f"singularity exec {singularity_exe} WisecondorX newref {out}/**/*.wcx.npz "
        f"{out.rstrip('/')}.test.npz --nipt --binsize {binsize}"
    )
    return cmd


def mkref(
    singularity_exe: str, config: dict, out: str, testbinsize: str, prefacebinsize: str
) -> str:
    """Command to generate wisecondorX reference files"""
    wcx_mkref = get_newref_cmd(
        config["singularity"], out, config["wisecondorx"]["testbinsize"]
    )

    wcx_mkrefpreface = get_newref_cmd(
        config["singularity"], out, config["wisecondorx"]["prefacebinsize"]
    )

    return "\n".join([wcx_mkref, wcx_mkrefpreface])
