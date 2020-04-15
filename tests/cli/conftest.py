"""Fixtures for cli"""

import pytest


@pytest.fixture(name="base_context")
def base_context_fixture(configs, samples, slurm_api, samplesheet_path):
    """Create a base context"""
    return {
        "samples": samples,
        "configs": configs,
        "sample_sheet": samplesheet_path,
        "slurm_api": slurm_api,
    }
