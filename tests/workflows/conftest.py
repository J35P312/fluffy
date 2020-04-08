"""fixtures for the workflow tests"""

import pytest


@pytest.fixture(name="sample_single")
def fixture_fixtures_dir() -> dict:
    """Return the a sample dictionary"""
    _sample = {
        "fastq": "<( zcat read_R1.fastq.gz )",
        "single_end": True,
        "sample_id": "single",
    }
    return _sample
