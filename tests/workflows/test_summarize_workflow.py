"""Tests for the align workflow"""

from fluffy.workflows.summarize import summarize_workflow


def test_xtest_workflow(configs, slurm_api, jobid):
    """Test to run x test workflow"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    summarize_jobid = summarize_workflow(
        configs=configs, dependencies=[jobid], slurm_api=slurm_api, dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert summarize_jobid == jobid
