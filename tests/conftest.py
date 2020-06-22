"""Fixtures for tests"""

import copy
import logging
import shutil
import sys
from pathlib import Path
from typing import Iterator

import pytest
from slurmpy import Slurm

from fluffy.config import get_configs
from fluffy.slurm_api import SlurmAPI

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

LOG = logging.getLogger("testing")


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


@pytest.fixture(scope="function", name="out_dir")
def fixture_out_dir(tmpdir_factory) -> Path:
    """Path to a temporary output directory"""
    my_tmpdir = Path(tmpdir_factory.mktemp("out"))
    yield my_tmpdir
    shutil.rmtree(str(my_tmpdir))


# file paths fixtures


@pytest.fixture(name="config_path")
def config_path_fixture(fixtures_dir: Path) -> Path:
    """Return the path to a config file"""
    _file_path = fixtures_dir / "config.json"
    return _file_path


@pytest.fixture(name="samplesheet_path")
def samplesheet_path_fixture(fixtures_dir: Path) -> Path:
    """Return the path to a config file"""
    _file_path = fixtures_dir / "samplesheet.csv"
    return _file_path


@pytest.fixture(name="configs")
def configs_fixture(config_path: Path, out_dir: Path, samplesheet_path: Path) -> dict:
    """Return test configs"""
    _configs = get_configs(config_path)
    _configs["out"] = out_dir
    _configs["sample_sheet"] = samplesheet_path
    return _configs


@pytest.fixture(name="account")
def account_fixture(configs: dict) -> str:
    """Return test account"""
    return configs["slurm"]["account"]


@pytest.fixture(name="jobid")
def jobid_fixture() -> int:
    """Return a jobid"""
    return 44444


# Sample fixtures


@pytest.fixture(name="sample_single")
def fixture_sample_single() -> dict:
    """Return the a sample dictionary"""
    _sample = {
        "fastq": "<( zcat read_R1.fastq.gz )",
        "single_end": True,
        "sample_id": "single",
    }
    return _sample


@pytest.fixture(name="samples")
def fixture_samples(sample_single) -> Iterator[dict]:
    """Return a iterable with samples"""
    _samples = []
    sample_id = sample_single["sample_id"]
    for number in range(3):
        sample = copy.deepcopy(sample_single)
        sample["sample_id"] = "_".join([sample_id, str(number)])
        _samples.append(sample)
    return _samples


# Slurm api fixtures


@pytest.fixture(name="real_slurm_api")
def real_slurm_api_fixture(configs, out_dir):
    """Return a real slurm API"""
    _api = SlurmAPI(
        slurm_settings=configs["slurm"],
        out_dir=out_dir,
    )
    return _api


@pytest.fixture(name="slurm_api")
def slurm_api_fixture(configs, out_dir, jobid):
    """Return a real slurm API"""
    _api = MockSlurmAPI(
        slurm_settings=configs["slurm"],
        out_dir=out_dir,
        _jobid=jobid,
    )

    return _api


class MockSlurmAPI:
    """Mock the slurm api"""

    def __init__(
        self, slurm_settings: dict, out_dir: Path, _jobid: int
    ):
        LOG.info("Initializing a slurm API")
        self.account = slurm_settings["account"]
        self.time = slurm_settings["time"]
        self.log_dir = out_dir / "logs"
        self.scripts_dir = out_dir / "scripts"
        self.slurm_settings=copy.copy(slurm_settings)
        self.job = None
        self._jobid = _jobid

    def create_job(self, name: str) -> Slurm:
        """Create a job for submitting to SLURM"""
        LOG.info("Create a slurm job with name %s", name)
        job = Slurm(
            name,
            {"account": self.account, "time": self.time,},
            scripts_dir=str(self.scripts_dir),
            log_dir=str(self.log_dir),
        )
        return job

    def run_job(
        self, name: str, command: str, afterok: list = None,afternotok: list = None, dry_run: bool = False,
    ) -> int:
        """Create and submit a job to slurm"""
        LOG.info("Submitting commands %s", command)
        if afterok:
            LOG.info(
                "Adding dependencies: %s", ",".join([str(dep) for dep in afterok])
            )
        jobid = 1
        if not dry_run:
           jobid = self._jobid
        LOG.info("Submitted job %s with job id: %s", name, jobid)
        return jobid

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(account={self.account!r}, time={self.time!r}, "
            f"log_dir={self.log_dir!r}, scripts_dir={self.scripts_dir!r}"
        )
