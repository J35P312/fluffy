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
    deliverables["files"].append({"format":"csv", "id":project_name,"path":str(summary_path),"step":"summarise_batch","tag":"NIPT_csv"})

    for sample in samples:
        sample_id=sample["sample_id"]
        zip_path=output_dir.absolute() / f"{sample_id}.fluffy-{__version__}.zip"
        deliverables["files"].append({"format":"zip", "id":sample_id,"path":str(zip_path),"step":"cleanup","tag":"fluffy_zip"})

    f=open(f"{str(output_dir)}/deliverables.yaml","w")
    f.write(yaml.dump(deliverables))
    f.close()
