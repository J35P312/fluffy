"""Code to check config"""

import json
import logging
import pathlib

LOG = logging.getLogger(__name__)


def file_exists(file_path: pathlib.Path) -> bool:
    """Check if a file exists.

    """
    if not file_path.exists():
        LOG.error("Could not find file %s", file_path)
        raise FileNotFoundError

    return True


def check_configs(config: dict, mkref: bool = False, skip_preface: bool = False):
    """Check if all files specified in config exists"""
    file_exists(pathlib.Path(config["reference"]))
    file_exists(pathlib.Path(config["wisecondorx"]["blacklist"]))
    file_exists(pathlib.Path(config["singularity"]))

    if mkref is False:
        file_exists(pathlib.Path(config["wisecondorx"]["reftest"]))

        if skip_preface is False:
            file_exists(pathlib.Path(config["wisecondorx"]["refpreface"]))


def get_configs(config_path: pathlib.Path) -> dict:
    """Parse and return configs"""

    with open(config_path) as config_handle:
        configs = json.load(config_handle)

    return configs
