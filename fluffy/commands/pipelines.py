"""Pipeline commands that uses multiple tools"""

import pathlib

from .bwa import (get_align_command, get_bamsormadup_command,
                  get_sampe_command, get_samse_command)
from .utils import get_outprefix
from .wisecondor import get_convert_cmd


def align_and_convert_single_end(
    config: dict, fastq: str, out: pathlib.Path, sample_id: str
) -> str:
    """create a command for running bwa and wisecondorX convert (single end)"""

    out_prefix = get_outprefix(out, sample_id)
    aln = get_align_command(
        singularity_exe=config["singularity"],
        reference=config["reference"],
        fastq=fastq,
        out_prefix=out_prefix,
    )

    samse_cmd = get_samse_command(
        singularity_exe=config["singularity"],
        reference=config["reference"],
        fastq=fastq,
        out_prefix=out_prefix,
    )
    bamsormadup_cmd = get_bamsormadup_command(
        singularity_exe=config["singularity"],
        tmp_dir=config["align"]["tmpdir"],
        sample_id=sample_id,
        out_prefix=out_prefix,
    )

    samse = " | ".join([samse_cmd, bamsormadup_cmd])

    convert = get_convert_cmd(
        singularity_exe=config["singularity"], out_prefix=out_prefix
    )

    return "\n".join([aln, samse, convert])


def align_and_convert_paired_end(
    config: dict, fastq: list, out: pathlib.Path, sample_id: str
) -> str:
    """create a command for running bwa and wisecondorX convert (paired end)"""
    out_prefix = get_outprefix(out, sample_id)
    aln_r1 = get_align_command(
        singularity_exe=config["singularity"],
        reference=config["reference"],
        fastq=fastq[0],
        out_prefix=out_prefix,
        read="r1",
    )

    aln_r2 = get_align_command(
        singularity_exe=config["singularity"],
        reference=config["reference"],
        fastq=fastq[1],
        out_prefix=out_prefix,
        read="r2",
    )

    sampe_cmd = get_sampe_command(
        singularity_exe=config["singularity"],
        reference=config["reference"],
        fastq1=fastq[0],
        fastq2=fastq[1],
        out_prefix=out_prefix,
    )

    bamsormadup_cmd = get_bamsormadup_command(
        singularity_exe=config["singularity"],
        tmp_dir=config["align"]["tmpdir"],
        sample_id=sample_id,
        out_prefix=out_prefix,
    )

    sampe = " | ".join([sampe_cmd, bamsormadup_cmd])

    convert = get_convert_cmd(
        singularity_exe=config["singularity"], out_prefix=out_prefix
    )

    return "\n".join([aln_r1, aln_r2, sampe, convert])
