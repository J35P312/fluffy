"""Code to align reads of a sample on SLURM"""

import logging

from fluffy.commands.pipelines import (align_and_convert_paired_end,
                                       align_and_convert_single_end,
                                       align_bwa_mem,align_bowtie2)
from fluffy.slurm_api import SlurmAPI

LOG = logging.getLogger(__name__)


def align_individual(
    configs: dict, sample: dict, slurm_api: SlurmAPI, dry_run: bool = False,bowtie2: bool = False,bwa_mem: bool = False
):
    """Align a individual with bwa on slurm"""
    out_dir = configs["out"]
    sample_id = sample["sample_id"]
    LOG.info("Aligning reads for %s", sample_id)
    single_end = sample["single_end"]
    fastq = sample["fastq"]

    if single_end:
        run_align = align_and_convert_single_end(
            config=configs, fastq=fastq[0], out=out_dir,sample_id=sample_id
        )
    elif bwa_mem:
        run_align=align_bwa_mem(
            config=configs, fastq=fastq, out=out_dir, sample_id=sample_id,single_end=single_end
        )

    elif bowtie2:
        run_align=align_bowtie2(
            config=configs, fastq=fastq, out=out_dir, sample_id=sample_id,single_end=single_end
        )
    else:
        run_align = align_and_convert_paired_end(
            config=configs, fastq=fastq, out=out_dir, sample_id=sample_id
        )

    align_jobid = slurm_api.run_job(
        name=f"FluffyAln-{sample_id}", command=run_align, dry_run=dry_run
    )


    return align_jobid
