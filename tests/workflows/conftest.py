"""fixtures for the workflow tests"""

from typing import Iterator

import pytest


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
    for _ in range(3):
        _samples.append(sample_single)
    return _samples
