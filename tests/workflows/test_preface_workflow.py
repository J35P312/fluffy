"""Tests for the align workflow"""

from fluffy.workflows.preface import preface_predict_workflow


def test_preface_predict_workflow(configs, slurm_api, sample_single, jobid):
    """Test to run preface predict workflow"""
    # GIVEN some configs, a mocked slurm api, a sample with one read and a jobid
    # WHEN running the align individual workflow
    preface_predict_jobid = preface_predict_workflow(
        configs=configs,
        sample_id=sample_single["sample_id"],
        afterok=jobid,
        slurm_api=slurm_api,
        dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert preface_predict_jobid == jobid
