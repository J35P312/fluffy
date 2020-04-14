"""Summarize the analysis"""

from pathlib import Path
from slurmpy import Slurm

def get_summarise_cmd(
    singularity_exe: str, out_dir: Path, sample_sheet: str, zscore: str, mincnv: str
) -> str:
    """Return a string with the command to summarize a run"""
    outfile = out_dir / "summary.csv"
    summary_cmd = (
        f"singularity exec {singularity_exe} python /bin/FluFFyPipe/scripts/generate_csv.py "
        f"--folder {str(out_dir)} --samplesheet {sample_sheet} --Zscore {zscore} --minCNV {mincnv} "
        f"> {str(outfile)}"
    )
    return summary_cmd


def summarize_workflow(configs: dict, out_dir: Path, jobids: list) -> int:
    """Run the workflow to summarize an analysis"""

    summarise_cmd = get_summarise_cmd(
        singularity_exe=configs["singularity"],
        out_dir=out_dir,
        sample_sheet=configs["sample_sheet"],
        zscore=configs["summary"]["zscore"],
        mincnv=configs["summary"]["mincnv"],
    )

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    summarise_batch = Slurm(
        "summarise_batch",
        configs["slurm"],
        log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )
    jobid = summarise_batch.run(summarise_cmd, depends_on=jobids)

    return jobid
