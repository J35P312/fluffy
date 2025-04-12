"""Commands to communicate with wcx2cytosure"""
""" Arguments are paths to wcx2cytosure_singularity, name of outfile, path to bins.bed and aberrations.bed. All as strings."""


def get_wcx2cytosure_cmd(singularity: str, out_prefix: str, wisecondorx_cov: str, wisecondorx_aberrations: str, tiddit_cov: str):
	wcx2cytosure_cmd = (
	
	f"{singularity} wcx2cytosure "
	f"--out {out_prefix} "
	f"--wisecondorx_cov {wisecondorx_cov} "
	f"--wisecondorx_aberrations {wisecondorx_aberrations} "
	f"--tiddit_cov {tiddit_cov} "
	)

	return wcx2cytosure_cmd
