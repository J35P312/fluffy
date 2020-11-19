"""Code to print deliverables file"""

import logging
import yaml

from pathlib import Path
from typing import Iterator

from fluffy.version import __version__

LOG = logging.getLogger(__name__)

def print_deliverables(output_dir: Path,project_dir: Path, samples: list) -> None:
    """Create a deliverables YAML file"""

    deliverables={"files":[]}
    project_name=project_dir.parent.name
    summary_path=output_dir.absolute() / "summary.csv"
    multiqc_path=output_dir.absolute() / "multiqc_report.html"

    deliverables["files"].append({"format":"csv", "id":project_name,"path":str(summary_path),"step":"summarise_batch","tag":"NIPT_csv"})
    deliverables["files"].append({"format":"html", "id":project_name,"path":str(multiqc_path),"step":"summarise_batch","tag":"MultiQC"})

    for sample in samples:
        sample_id=sample["sample_id"]
        zip_path=output_dir.absolute() / f"{sample_id}.WCXpredict_abberations.filt.bed"
        deliverables["files"].append({"format":"bed", "id":sample_id,"path":str(zip_path),"step":"wcx","tag":"Wisecondor_abberations"})

    f=open(f"{str(output_dir)}/deliverables.yaml","w")
    f.write(yaml.dump(deliverables))
    f.close()
