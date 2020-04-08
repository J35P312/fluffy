"""Fixtures for tests"""

import logging
import shutil
import sys
from pathlib import Path

import pytest

from fluffy.config import get_configs
from fluffy.slurm_api import SlurmAPI

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@pytest.fixture(name="fixtures_dir")
def fixture_fixtures_dir() -> Path:
    """Return the path to a the fixtures dir"""
    _dir_path = Path("tests/fixtures")
    return _dir_path


# Temp files fixtures #


@pytest.fixture(scope="function", name="project_dir")
def fixture_project_dir(tmpdir_factory) -> Path:
    """Path to a temporary directory"""
    my_tmpdir = Path(tmpdir_factory.mktemp("data"))
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


# file paths fixtures


@pytest.fixture(name="config_path")
def config_path_fixture(fixtures_dir: Path) -> Path:
    """Return the path to a config file"""
    _file_path = fixtures_dir / "config.json"
    return _file_path


@pytest.fixture(name="configs")
def configs_fixture(config_path: Path) -> dict:
    """Return test configs"""
    return get_configs(config_path)


@pytest.fixture(name="account")
def account_fixture(configs: dict) -> str:
    """Return test account"""
    return configs["slurm"]["account"]


@pytest.fixture(name="real_slurm_api")
def real_slurm_api_fixture(configs, project_dir):
    """Return a real slurm API"""
    _api = SlurmAPI(
        account=configs["slurm"]["account"],
        time=configs["slurm"]["time"],
        out_dir=project_dir,
    )
    return _api
