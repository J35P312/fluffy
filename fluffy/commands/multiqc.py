"""Commands that use multiqc"""
from pathlib import Path

def get_multiqc_cmd(singularity: str, input_dir: Path, out_dir: Path) -> str:
    """Get command for generating multiqc report"""
    cmd = (
	f"{singularity} /bin/bash -c \"source activate multiqc; multiqc {str(input_dir)} --outdir {str(out_dir)}\""
    )
    return cmd
