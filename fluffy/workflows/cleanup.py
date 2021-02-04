"""Make a cleaned up per sample zip file"""

from pathlib import Path

from fluffy.slurm_api import SlurmAPI
from fluffy.version import __version__
from fluffy.commands.multiqc import get_multiqc_cmd
from fluffy.singularity_cmd import singularity_base

def get_cleanup_cmd(out_dir: Path, sample_outdir: Path, sample_id: str) -> str:
    """Return a string with the command to clean up and compress a sample run folder"""
    sample_results_file = f"{str(out_dir)}/{sample_id}.fluffy-{__version__}"

    cleanup_cmd = (
        f"cp -r {sample_outdir} {sample_results_file}; "
        f"rm -f {sample_results_file}/*.sai {sample_results_file}/*.bam; "
        f"zip -r {sample_results_file}.zip {sample_results_file}; "
        f"rm -rf {sample_results_file}"
    )
    return cleanup_cmd


def cleanup_workflow(
    configs: dict,
    sample_outdir: Path,
    sample_id: str,
    afterok: list,
    slurm_api: SlurmAPI,
    dry_run: bool = False,
) -> int:
    """Run the workflow to compress  an analysis folder"""

    out_dir = configs["out"]
    cleanup_cmd = get_cleanup_cmd(
        out_dir=out_dir, sample_outdir=sample_outdir, sample_id=sample_id,
    )

    singularity=singularity_base(configs["singularity"], configs["out"], configs["project"], configs["singularity_bind"])

    multiqc_cmd=get_multiqc_cmd(singularity=singularity,input_dir=sample_outdir,out_dir=sample_outdir)

    jobid = slurm_api.run_job(
        name=f"cleanup-{sample_id}",
        command="\n".join([multiqc_cmd,cleanup_cmd]),
        afterok=afterok,
        dry_run=dry_run,
    )

    return jobid
