"""Commands that use multiqc"""
from pathlib import Path

def get_multiqc_cmd(singularity_exe: str, input_dir: Path, out_dir: Path) -> str:
    """Get command for converting bam to called nipt"""
    cmd = (
	f"singularity exec {singularity_exe} multiqc {str(input_dir)} --outdir {str(out_dir)}"
    )
    return cmd
