"""Code to handle samplesheets"""

import logging
from pathlib import Path
from typing import Iterator

LOG = logging.getLogger(__name__)


def get_separator(line: str) -> str:
    """Get the separator for file"""
    if " " in line:
        return " "
    if "," in line:
        return ","
    return None


def get_sample_col(line_content: list) -> int:
    """Get the column number that holds the sample name"""
    for column, info in enumerate(line_content):
        if info.lower() == "sampleid":
            return column
    return None

def get_project_col(line_content: list) -> int:
    """Get the column number that holds the sample name"""
    for column, info in enumerate(line_content):
        if info.lower() == "project":
            return column
    return None

def get_sample_name_col(line_content: list) -> int:
    """Get the column number that holds the sample name"""
    for column, info in enumerate(line_content):
        if info.lower() == "samplename":
            return column
    return None


def read_samplesheet(samplesheet: Iterator[str], project_dir: Path) -> Iterator[dict]:
    """Parse a sample sheet and return sample information

    Yields:
        samples(dict): a dictionary with a list of commands and 'se'(bool)
    """

    samples = set()
    sample_col = 0
    project_col=0

    first=True
    for line_nr, line in enumerate(samplesheet):

        if line.startswith("[Data]") and first:
            continue

        if first:
            separator = get_separator(line)
            LOG.debug("Use separator %s", separator)
            header = line.rstrip().split(separator)
            sample_col = get_sample_col(header)
            sample_name_col = get_sample_name_col(header)
            project_col = get_project_col(header)
            first=False
            continue

        content = line.rstrip().split(separator)
        sample_name = content[sample_col]

        if sample_name in samples:
            continue

        samples.add(sample_name)

        single_end = True
        LOG.debug("Check if files are single end or not")
        for file_name in project_dir.glob(f"*{sample_name}*/*.fastq.gz"):
            if "_R2" in str(file_name):
                single_end = False
                break

        fastq = [
            "<( zcat {}/*{}/*_R1*fastq.gz )".format(project_dir, sample_name),
            "<( zcat {}/*{}/*_R2*fastq.gz )".format(project_dir, sample_name),
        ]
        if single_end:
            LOG.info("Single end files!")
            fastq = ["<( zcat {}/*{}/*_R1*fastq.gz )".format(project_dir, sample_name)]

        if sample_name_col:
           sample_name = content[sample_name_col]

        if project_col:
           sample_project=content[project_col]
        else:
           sample_project="summary"

        yield {"fastq": fastq, "single_end": single_end, "sample_id": sample_name, "project":sample_project }
