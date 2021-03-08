"""Code to print analysis status json file"""

import logging
import json
import os

from pathlib import Path
from typing import Iterator
import sys

from datetime import datetime
from fluffy.version import __version__

LOG = logging.getLogger(__name__)

def check_status(output_dir: Path) -> None:
    """Check the analysis status"""
    if os.path.exists(f'{str(output_dir)}/analysis_status.json'):
       f = open(f'{str(output_dir)}/analysis_status.json')
       status=json.load(f)
       return(status)

    else:
       return(False)

def print_status(output_dir: Path) -> None:
    """Create a status json file"""

    analysis_time=datetime.now()
    time_string=f"{analysis_time.year}-{analysis_time.month}-{analysis_time.day}T{analysis_time.hour}:{analysis_time.minute}:{analysis_time.second}"

    analysis_status={"analysis_run_status":"running","analysis_command":" ".join(sys.argv),"analysis_time":time_string,"fluffy_version":__version__}
    f=open(f"{str(output_dir)}/analysis_status.json","w")
    f.write(json.dumps(analysis_status))
    f.close()
    return(analysis_status)


