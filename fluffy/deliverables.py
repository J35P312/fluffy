"""Code to print deliverables file"""

import logging
import yaml

from pathlib import Path
from typing import Iterator

from fluffy.version import __version__

LOG = logging.getLogger(__name__)

def print_deliverables(output_dir: Path,project_dir: Path, samples: list,batch_ref=bool, project_id = "summary") -> None:
    """Create a deliverables YAML file"""

    deliverables={"files":[]}
    project_name=str(output_dir).strip("/").split("/")[-1]
    summary_path=output_dir.absolute() / f"{project_id}.csv"
    summary_first_pass_path=output_dir.absolute() / f"{project_id}.1pass.csv"
    summary_second_pass_path=output_dir.absolute() / f"{project_id}.2pass.csv"

    multiqc_path=output_dir.absolute() / "multiqc_report.html"
    
    if batch_ref:
        deliverables["files"].append({"format":"csv", "id":project_name,"path":str(summary_first_pass_path),"step":"summarise_batch","tag":"NIPT_first_pass_csv"})
        deliverables["files"].append({"format":"csv", "id":project_name,"path":str(summary_second_pass_path),"step":"summarise_batch","tag":"NIPT_second_pass_csv"})
 
    deliverables["files"].append({"format":"csv", "id":project_name,"path":str(summary_path),"step":"summarise_batch","tag":"NIPT_csv"})
    deliverables["files"].append({"format":"html", "id":project_name,"path":str(multiqc_path),"step":"summarise_batch","tag":"MultiQC"})

    for sample in samples:
        sample_id=sample["sample_id"]
        zip_path=output_dir.absolute() / f"{sample_id}/{sample_id}.WCXpredict_aberrations.filt.bed"
        deliverables["files"].append({"format":"bed", "id":sample_id,"path":str(zip_path),"step":"summarise_batch","tag":"Wisecondor_aberrations"})

    f=open(f"{str(output_dir)}/deliverables.yaml","w")
    f.write(yaml.dump(deliverables))
    f.close()
