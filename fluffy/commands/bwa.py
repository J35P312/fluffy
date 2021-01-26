"""Commands that use bwa"""


def get_align_command(
    singularity: str, sample_id: str,tmp_dir: str, reference: str, fastq: str,out_dir:str, out_prefix: str, read: str = None
) -> str:
    """create a command to run bwa align. Read can be r1, r2 or none"""
    read_prefix = ".sai"
    if read == "r1":
        read_prefix = "_R1.sai"
    if read == "r2":
        read_prefix = "_R2.sai"

    fastqc_prefix=read_prefix.replace(".sai","")
    cmd = (
        f"{singularity} bwa aln -n 0 -k 0 {reference} {fastq} > "
        f"{out_prefix}{read_prefix}\n"
        f"{singularity} cat {fastq} | {singularity} fastqc stdin:{sample_id}{fastqc_prefix} -d {tmp_dir} -o {out_dir}/{sample_id}"
    )
    return cmd


def get_samse_command(
    singularity: str, reference: str, fastq: str, out_prefix: str
) -> str:
    """create a command for running bwa samsw"""
    cmd = f"{singularity} bwa samse -n -1 {reference} {out_prefix}.sai {fastq}"
    return cmd


def get_sampe_command(
    singularity: str, reference: str, fastq1: str, fastq2: str, out_prefix: str
) -> str:
    """create a command for running bwa sampe"""
    cmd = (
        f"{singularity} bwa sampe -n -1 {reference} "
        f"{out_prefix}_R1.sai {out_prefix}_R2.sai {fastq1} {fastq2}"
    )
    return cmd


def get_bamsormadup_command(
    singularity: str, tmp_dir: str, sample_id: str, out_prefix: str
) -> str:
    """Create a command for running bamorsamdup"""
    cmd = (
        f"{singularity} bamsormadup inputformat=sam threads=16 SO=coordinate "
        f"outputformat=bam tmpfile={tmp_dir}/{sample_id} "
        f"indexfilename={out_prefix}.bam.bai > {out_prefix}.bam"
    )
    return cmd
