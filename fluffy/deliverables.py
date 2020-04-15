"""Code to print deliverables file"""

import logging
import yaml

from pathlib import Path
from typing import Iterator

from fluffy.version import __version__

LOG = logging.getLogger(__name__)

def print_deliverables(output_dir: Path,project_dir: Path, samples: Iterator[dict]) -> None:
    """Create a deliverables YAML file"""

    deliverables={"Files":[]}
    project_name=str(project_dir).strip("/").split("/")[-1]
    summary_path=f"{output_dir.absolute}/summary.csv"
    deliverables["Files"].append({"format":"csv", "id":project_name,"path":summary_path,"step":"summarise_batch","tag":"NIPT_csv"})

    for sample in samples:
        zip_path=f"{output_dir.absolute}/{sample}.fluffy-{__version__}.zip"
        deliverables["Files"].append({"format":"zip", "id":sample,"path":zip_path,"step":"cleanup","tag":"fluffy_zip"})

    print(yaml.dump(deliverables))
