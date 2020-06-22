"""Tests for the align workflow"""

from fluffy.workflows.amycne import estimate_ffy


def test_estimate_ffy(configs, slurm_api, sample_single, jobid):
    """Test to run align individual"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    estimate_jobid = estimate_ffy(
        configs=configs,
        sample_id=sample_single["sample_id"],
        afterok=jobid,
        slurm_api=slurm_api,
        dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert estimate_jobid == jobid
