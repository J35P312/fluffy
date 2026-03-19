"""Commands that use Spiky python cli"""

def get_spiky_cmd(
    singularity: str, out_prefix: str, spiky_model: str, spiky_regions: str, bin_size:int, reference:str) -> str:
    """Get a string with command for running AMYCNEs fetal fraction

    This will predict the gender and how much dna is a sample is from the fetus.
    """
    spiky_predict_cmd = (
        f"{singularity} spiky --coverage-bed --bin-size {bin_size} --reference-fasta {reference} --bam {out_prefix}.bam > {out_prefix}.spiky.bed\n"
        f"{singularity} spiky  --predict --coverage-bed-file {out_prefix}.spiky.bed --regions-bed {spiky_regions} --model-file {spiky_model} > "
        f"{out_prefix}.tiddit.AMYCNE.tab\n"
    )
    return spiky_predict_cmd
