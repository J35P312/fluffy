"""Make a cleaned up per sample zip file"""

from pathlib import Path
from slurmpy import Slurm
from fluffy.version import __version__

def get_cleanup_cmd(
    out_dir: Path, sample_outdir: Path, sample_id: str
) -> str:
    """Return a string with the command to clean up and compress a sample run folder"""
    sample_results_file= f"{str(out_dir)}/{sample_id}.fluffy-{__version__}"

    cleanup_cmd = (

        f"cp -r {sample_outdir} {sample_results_file}; "
        f"rm -f {sample_results_file}/*.sai {sample_results_file}/*.bam; "
        f"zip -r {sample_results_file}.zip {sample_results_file}; "
        f"rm -rf {sample_results_file}"

    )
    return cleanup_cmd

def cleanup_workflow(configs: dict, out_dir: Path, sample_outdir: Path, sample_id: str, sample_jobids: list) -> int:
    """Run the workflow to summarize an analysis"""

    cleanup_cmd = get_cleanup_cmd(
	out_dir=out_dir,
        sample_outdir=sample_outdir,
        sample_id=sample_id,
    )

    log_dir = out_dir / "logs"
    scripts_dir = out_dir / "scripts"

    cleanup_batch = Slurm(
        f"cleanup-{sample_id}",
        configs["slurm"],
	log_dir=str(log_dir),
        scripts_dir=str(scripts_dir),
    )
    jobid = cleanup_batch.run(cleanup_cmd, depends_on=sample_jobids)

    return jobid
