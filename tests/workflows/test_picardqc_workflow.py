"""Tests for the align workflow"""

from fluffy.workflows.picard import picard_qc_workflow


def test_picard_qc(configs, slurm_api, sample_single, jobid):
    """Test to run align individual"""
    # GIVEN some configs, a mocked slurm api, a sample with ine read and a jobid
    # WHEN running the align individual workflow
    picard_jobid = picard_qc_workflow(
        configs=configs,
        sample_id=sample_single["sample_id"],
        afterok=jobid,
        slurm_api=slurm_api,
        dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert picard_jobid == jobid
