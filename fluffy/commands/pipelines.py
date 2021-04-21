"""Pipeline commands that uses multiple tools"""

from pathlib import Path

from .amycne import get_gctab_cmd, run_amycne_cmd
from .bwa import (get_align_command, get_bamsormadup_command,
                  get_sampe_command, get_samse_command)
from fluffy.singularity_cmd import singularity_base
from .picard import (get_collect_gc_bias_cmd, get_collect_insert_size_cmd,
                     get_estimate_complexity_cmd)
from .tiddit import get_tiddit_cmd
from .utils import get_outprefix
from .wisecondor import get_convert_cmd, get_gender_cmd, get_predict_cmd


def align_and_convert_single_end(
    config: dict, fastq: str, out: Path, sample_id: str
) -> str:
    """create a command for running bwa and wisecondorX convert (single end)"""

    singularity=singularity_base(config["singularity"], config["out"], config["project"], config["singularity_bind"])

    out_prefix = get_outprefix(out, sample_id)
    aln = get_align_command(
        singularity=singularity,
        sample_id=sample_id,
        tmp_dir=config["align"]["tmpdir"],
        reference=config["reference"],
        fastq=fastq,
        out_dir=str(out),
        out_prefix=out_prefix,
    )

    samse_cmd = get_samse_command(
	singularity=singularity,
        reference=config["reference"],
        fastq=fastq,
        out_prefix=out_prefix,
    )
    bamsormadup_cmd = get_bamsormadup_command(
        singularity=singularity,
        tmp_dir=config["align"]["tmpdir"],
        sample_id=sample_id,
        out_prefix=out_prefix,
    )

    samse = " | ".join([samse_cmd, bamsormadup_cmd])

    convert = get_convert_cmd(
        singularity=singularity, out_prefix=out_prefix
    )

    return "\n".join([aln, samse, convert])


def align_and_convert_paired_end(
    config: dict, fastq: list, out: Path, sample_id: str
) -> str:
    """create a command for running bwa and wisecondorX convert (paired end)"""

    singularity=singularity_base(config["singularity"], config["out"], config["project"], config["singularity_bind"])

    out_prefix = get_outprefix(out, sample_id)
    aln_r1 = get_align_command(
        singularity=singularity,
       	sample_id=sample_id,
       	tmp_dir=config["align"]["tmpdir"],
        reference=config["reference"],
        fastq=fastq[0],
       	out_dir=str(out),
        out_prefix=out_prefix,
        read="r1",
    )

    aln_r2 = get_align_command(
        singularity=singularity,
       	sample_id=sample_id,
       	tmp_dir=config["align"]["tmpdir"],
        reference=config["reference"],
        fastq=fastq[1],
       	out_dir=str(out),
        out_prefix=out_prefix,
        read="r2",
    )

    sampe_cmd = get_sampe_command(
        singularity=singularity,
        reference=config["reference"],
        fastq1=fastq[0],
        fastq2=fastq[1],
        out_prefix=out_prefix,
    )

    bamsormadup_cmd = get_bamsormadup_command(
        singularity=singularity,
        tmp_dir=config["align"]["tmpdir"],
        sample_id=sample_id,
        out_prefix=out_prefix,
    )

    sampe = " | ".join([sampe_cmd, bamsormadup_cmd])

    convert = get_convert_cmd(
        singularity=singularity, out_prefix=out_prefix
    )

    return "\n".join([aln_r1, aln_r2, sampe, convert])


def amycne_ffy(configs: dict, out_dir: Path, sample_id: str) -> str:
    """fetal fraction estimation using tiddit and AMYCNE"""
    out_prefix = out_dir / sample_id / sample_id
    path_gc_tab = out_dir / sample_id / ".".join([sample_id, "gc.tab"])

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    # Calculate coverage bins with tiddit
    tiddit_cmd = get_tiddit_cmd(
        singularity=singularity,
        out_prefix=str(out_prefix),
        binsize=configs["tiddit"]["binsize"],
    )

    # Calculate bins with GC and quality filtering
    gc_tab_cmd = get_gctab_cmd(
        singularity=singularity,
        reference=configs["reference"],
        binsize=configs["tiddit"]["binsize"],
        path_gc_tab=str(path_gc_tab),
    )

    amycne_cmd = run_amycne_cmd(
        singularity=singularity,
        out_prefix=str(out_prefix),
        path_gc_tab=str(path_gc_tab),
        minq=configs["amycne"]["minq"],
    )
    return "\n".join([tiddit_cmd, gc_tab_cmd, amycne_cmd])


def picard_qc(configs: dict, out_dir: Path, sample_id: str) -> str:
    """Get a string with pipeline steps to run picard qc"""
    out_prefix = out_dir / sample_id / sample_id
    reference = configs["reference"]
    javasettings = configs["picard"]["javasettings"]

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    gc_bias_cmd = get_collect_gc_bias_cmd(
        singularity=singularity,
        out_prefix=str(out_prefix),
        reference=reference,
        javasettings=javasettings,
        tmp_dir=str(configs["align"]["tmpdir"]),
    )

    insert_size_cmd = get_collect_insert_size_cmd(
        singularity=singularity,
        out_prefix=str(out_prefix),
        javasettings=javasettings,
        tmp_dir=str(configs["align"]["tmpdir"]),
    )

    estimate_complexity_cmd = get_estimate_complexity_cmd(
        singularity=singularity,
        out_prefix=str(out_prefix),
        javasettings=javasettings,
        tmp_dir=str(configs["align"]["tmpdir"]),
    )

    return "\n".join([gc_bias_cmd, insert_size_cmd, estimate_complexity_cmd])


def wisecondor_x_test(configs: dict, out_dir: Path, sample_id: str) -> str:
    """Get the commands for running the wisecondor chromosome X test"""
    out_prefix = out_dir / sample_id / sample_id
    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])
    blacklist = configs["wisecondorx"]["blacklist"]
    zscore = str(configs["wisecondorx"]["zscore"])

    wisecondor_test_cmd = get_predict_cmd(
        singularity=singularity,
        out_prefix=out_prefix,
        reference=configs["wisecondorx"]["reftest"],
        blacklist=blacklist,
        zscore=zscore,
    )

    wisecondor_preface_cmd = get_predict_cmd(
        singularity=singularity,
        out_prefix=out_prefix,
        reference=configs["wisecondorx"]["refpreface"],
        blacklist=blacklist,
        zscore=zscore,
        preface=True,
    )

    wisecondor_gender_cmd = get_gender_cmd(
        singularity=singularity,
        out_prefix=out_prefix,
        reference=configs["wisecondorx"]["reftest"],
    )

    return "\n".join(
        [wisecondor_test_cmd, wisecondor_preface_cmd, wisecondor_gender_cmd]
    )
