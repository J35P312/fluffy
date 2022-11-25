"""Commands that use bwa"""


def get_align_command(
    fastq: str,
    out_dir: str,
    out_prefix: str,
    reference: str,
    singularity: str,
    sample_id: str,
    threads: str,
    tmp_dir: str,
    read: str = None,
) -> str:
    """create a command to run bwa align. Read can be r1, r2 or none"""
    read_prefix = ".sai"
    if read == "r1":
        read_prefix = "_R1.sai"
    if read == "r2":
        read_prefix = "_R2.sai"

    fastqc_prefix = read_prefix.replace(".sai", "")
    cmd = (
        f"{singularity} bwa aln -n 0 -k 0 -t {threads} {reference} {fastq} > "
        f"{out_prefix}{read_prefix}\n"
        f"{singularity} cat {fastq} | "
        f"{singularity} fastqc stdin:{sample_id}{fastqc_prefix} -d {tmp_dir} -o {out_dir}/{sample_id}"
    )
    return cmd


def get_samse_command(
    fastq: str, out_prefix: str, reference: str, singularity: str, threads: str
) -> str:
    """create a command for running bwa samsw"""
    cmd = (
        f"{singularity} bwa samse -n -1 {reference} {out_prefix}.sai {fastq} | {singularity} samtools sort - "
        f"-@ {threads} -T {out_prefix}.tmp > {out_prefix}.tmp.bam"
    )
    return cmd


def get_sampe_command(
    fastq1: str,
    fastq2: str,
    out_prefix: str,
    reference: str,
    singularity: str,
    threads: str,
) -> str:
    """create a command for running bwa sampe"""
    cmd = (
        f"{singularity} bwa sampe -n -1 {reference} "
        f"{out_prefix}_R1.sai {out_prefix}_R2.sai {fastq1} {fastq2} | {singularity} samtools sort - -@ {threads} "
        f"-T {out_prefix}.tmp > {out_prefix}.tmp.bam"
    )
    return cmd


def get_bamsormadup_command(
    out_prefix: str, singularity: str, tmp_dir: str
) -> str:
    """Create a command for running bamorsamdup"""
    cmd = (
        f"{singularity} picard MarkDuplicates TMP_DIR={tmp_dir} I={out_prefix}.tmp.bam O={out_prefix}.bam "
        f"M={out_prefix}.md.txt CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
        f"rm {out_prefix}.tmp.bam"
    )
    return cmd
