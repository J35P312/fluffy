"""code to generate the singularity base command"""
import logging
from pathlib import Path

def singularity_base(singularity_exe: str, out_dir: Path, project_dir: Path, singularity_bind: list):
	bind=f" --bind {str(out_dir)} --bind {str(project_dir)}"
	if singularity_bind:
		for d in singularity_bind:
			bind+= f" --bind {d}"

	singularity_base_cmd= f"singularity exec {bind} {singularity_exe}"
	return singularity_base_cmd

