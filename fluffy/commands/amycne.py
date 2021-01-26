"""Commands that use AMYCNE python cli"""


def get_gctab_cmd(
    singularity: str, reference: str, binsize: str, path_gc_tab: str
) -> str:
    """Get a string with command to run the AMYCNE gc correction program.

    This is to identify problematic regions to exclude for AMYCNE fetal fraction and to
    do GC-correction
    """
    gc_tab_cmd = (
        f"{singularity} python /bin/AMYCNE/Generate_GC_tab.py "
        f"--fa {reference} --size {binsize} --n_mask > {path_gc_tab}"
    )

    return gc_tab_cmd


def run_amycne_cmd(
    singularity: str, out_prefix: str, path_gc_tab: str, minq: str
) -> str:
    """Get a string with command for running AMYCNEs fetal fraction

    This will predict the gender and how much dna is a sample is from the fetus.
    """
    amycne_cmd = (
        f"{singularity} python /bin/AMYCNE/AMYCNE.py --ff "
        f"--coverage {out_prefix}.tiddit.tab --gc {path_gc_tab} --Q {minq} > "
        f"{out_prefix}.tiddit.AMYCNE.tab"
    )
    return amycne_cmd
