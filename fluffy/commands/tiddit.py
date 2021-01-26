"""Commands to communicate with tiddit"""


def get_tiddit_cmd(singularity: str, out_prefix: str, binsize: str):
    """Return a string for command to calculate bins containing coverage values
    over the genome. This is done with Tiddit
    """
    tiddit_cmd = (
        f"{singularity} python /bin/TIDDIT.py --cov --bam {out_prefix}.bam "
        f" -z {binsize} -o {out_prefix}.tiddit"
    )

    return tiddit_cmd
