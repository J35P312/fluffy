"""Code to align reads of a sample on SLURM"""

import logging
from pathlib import Path

from slurmpy import Slurm

from fluffy.commands.pipelines import (align_and_convert_paired_end,
                                       align_and_convert_single_end)

LOG = logging.getLogger(__name__)


def align_individual(configs: dict, sample: dict, out_dir: Path, dry_run: bool = False):
    """Align a individual with bwa on slurm"""
    sample_id = sample["sample_id"]
    LOG.info("Aligning reads for %s", sample_id)
    single_end = sample["single_end"]
    fastq = sample["fastq"]
    if single_end:
        run_bwa = align_and_convert_single_end(
            config=configs, fastq=fastq[0], out=out_dir, sample_id=sample_id,
        )
    else:
        run_bwa = align_and_convert_paired_end(
            config=configs, fastq=fastq, out=out_dir, sample_id=sample_id,
        )
    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    bwa = Slurm(
        f"bwaAln-{sample_id}",
        {
            "account": configs["slurm"]["account"],
            "partition": "node",
            "time": configs["slurm"]["time"],
        },
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )
    align_jobid = None
    if not dry_run:
        align_jobid = bwa.run(run_bwa)

    return align_jobid
