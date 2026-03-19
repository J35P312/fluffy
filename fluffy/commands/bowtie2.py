"""Commands that use bowtie2"""

def get_bowtie2_command(
    singularity_fluffy: str,
    singularity_bowtie2: str,
    singularity_fastp: str,
    reference: str,
    threads: str,
    fastq: list,
    out_prefix: str,
    single_end: bool,
    sample_id: str,
    tmp_dir: str,
    out_dir: str,
) -> str:
     """Create a command for running bowtie2, only compatible with paired end reads"""

     cmd= ( 
        f"{singularity_fluffy} cat {fastq[0]} > {out_dir}/{sample_id}/{sample_id}_1.fq\n"
        f"{singularity_fluffy} cat {fastq[1]} > {out_dir}/{sample_id}/{sample_id}_2.fq\n"
        f"{singularity_fastp} fastp --in1 {out_dir}/{sample_id}/{sample_id}_1.fq --in2 {out_dir}/{sample_id}/{sample_id}_2.fq --out1 {out_dir}/{sample_id}/{sample_id}_R1.fq.gz --out2 {out_dir}/{sample_id}/{sample_id}_R2.fq.gz --json {out_dir}/{sample_id}/{sample_id}.json --html {out_dir}/{sample_id}/{sample_id}.fastp.html --thread {threads} --detect_adapter_for_pe --trim_poly_g\n"
        f"{singularity_bowtie2} bowtie2 -p {threads} -x {reference} -1 {out_dir}/{sample_id}/{sample_id}_R1.fq.gz -2 {out_dir}/{sample_id}/{sample_id}_R2.fq.gz --local | {singularity_fluffy} samtools sort - -@ {threads} "
        f"-T {out_prefix}.tmp > {out_prefix}.tmp.bam\n"
        f"rm {out_dir}/{sample_id}/{sample_id}_1.fq {out_dir}/{sample_id}/{sample_id}_2.fq"
        
        )

     return cmd
