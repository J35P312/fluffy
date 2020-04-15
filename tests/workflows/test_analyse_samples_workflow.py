"""Tests for the analyse samples workflow"""

from fluffy.workflows.analyse_samples import analyse_workflow


def test_analyse_samples_workflow(configs, slurm_api, samples, jobid):
    """Test to run analyse samples workflow"""
    # GIVEN some configs, a mocked slurm api, a iterable with samples and a jobid
    # WHEN running the analyse samples workflow

    analyse_samples_jobid = analyse_workflow(
        samples=samples,
        configs=configs,
        slurm_api=slurm_api,
        skip_preface=False,
        dry_run=False,
    )
    # THEN assert the correct jobid is returned
    assert analyse_samples_jobid == jobid
