"""Workflows to run picard"""

from pathlib import Path

from slurmpy import Slurm

from fluffy.commands.pipelines import picard_qc


def picard_qc_workflow(configs: dict, out_dir: Path, sample_id: str, align_jobid: int):
    """Run the picard pipeline"""
    picard_qc_pipe = picard_qc(configs=configs, out_dir=out_dir, sample_id=sample_id)

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    picard = Slurm(
        "picard_qc-{}".format(sample_id),
        configs["slurm"],
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )
    jobid = picard.run(picard_qc_pipe, depends_on=[align_jobid])

    return jobid
