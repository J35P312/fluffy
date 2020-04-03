"""Workflow for making a reference based on samples"""

import pathlib
from typing import Iterator

from fluffy.commands.pipelines import (align_and_convert_paired_end,
                                       align_and_convert_single_end)
from slurmpy import Slurm


def make_reference(
    samples: Iterator[dict], out_dir: pathlib.Path, configs: dict
) -> int:
    """docstring for make_reference"""
    jobids = []
    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"
    for sample in samples:
        sample_id = sample["sample_id"]
        if sample["single_end"]:
            run_bwa = align_and_convert_single_end(
                config=configs,
                fastq=sample["fastq"][0],
                out=out_dir,
                sample_id=sample_id,
            )
        else:
            run_bwa = align_and_convert_paired_end(
                config=config, fastq=sample["fastq"], out=out_dir, sample_id=sample_id,
            )

        bwa = Slurm(
            "bwaAln-{}".format(sample_id),
            {
                "account": config["slurm"]["account"],
                "partition": "node",
                "time": config["slurm"]["time"],
            },
            log_dir=str(log_dir),
            scripts_dir=str(scripts_dir),
        )
        jobids.append(bwa.run(run_bwa))

    wcxmkref = Slurm(
        "wcxmkref",
        {
            "account": config["slurm"]["account"],
            "partition": "node",
            "time": config["slurm"]["time"],
        },
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )
    job_id = wcxmkref.run(mkref(config, args), depends_on=jobids)

    return job_id
