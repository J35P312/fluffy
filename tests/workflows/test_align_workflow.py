"""Tests for the align workflow"""

from fluffy.workflows.align import align_individual


def test_align_individual_single(configs, slurm_api, sample_single, jobid):
    """Test to run align individual"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    align_jobid = align_individual(
        configs=configs, sample=sample_single, slurm_api=slurm_api, dry_run=False
    )
    # THEN assert the correct jobid is returned
    assert align_jobid == jobid
