"""fixtures for the workflow tests"""

import copy
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
    sample_id = sample_single["sample_id"]
    for number in range(3):
        sample = copy.deepcopy(sample_single)
        sample["sample_id"] = "_".join([sample_id, str(number)])
        _samples.append(sample)
    return _samples
