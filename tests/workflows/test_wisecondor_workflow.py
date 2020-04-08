"""Tests for the align workflow"""

from fluffy.workflows.wisecondor import (make_reference,
                                         wisecondor_xtest_workflow)


def test_xtest_workflow(configs, slurm_api, sample_single, jobid):
    """Test to run x test workflow"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    xtest_jobid = wisecondor_xtest_workflow(
        configs=configs,
        sample_id=sample_single["sample_id"],
        dependency=jobid,
        slurm_api=slurm_api,
        dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert xtest_jobid == jobid


def test_make_reference_workflow(configs, slurm_api, samples, jobid):
    """Test to make reference"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    makeref_jobid = make_reference(
        configs=configs, samples=samples, slurm_api=slurm_api, dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert makeref_jobid == jobid
