"""Tests for SLURM api"""

from pathlib import Path

from slurmpy import Slurm

from fluffy.slurm_api import SlurmAPI


def test_init():
    """Test to initialize a slurm api"""
    # GIVEN a acount, a time, an out dir
    account = "my_account"
    time = "5:00:00"
    out_dir = Path("tests/fixtures/output")
    # WHEN instantiating a slurm api
    api = SlurmAPI(slurm_settings={"account":account, "time":time}, out_dir=out_dir)
    # THEN assert it is setup correct
    assert api.account == account
    assert api.log_dir
    assert api.scripts_dir


def test_get_job(real_slurm_api):
    """Test to get a job from a slurm api"""
    # GIVEN a slurm api and a job name
    job_name = "test"
    # WHEN creating a slurm job
    slurm_job = real_slurm_api.create_job(name=job_name)
    # THEN assert a slutmpyjob was created
    assert isinstance(slurm_job, Slurm)


def test_submit_job(real_slurm_api):
    """Test to get a job from a slurm api"""
    # GIVEN a slurm api, a job name and a command
    job_name = "test"
    command = "tests/"
    # WHEN submitting a slurm job
    jobid = real_slurm_api.run_job(name=job_name, command=command, dry_run=True)
    # THEN assert a jobid is 1 since dry_run
    assert jobid == 1


def test_write_yaml_job(real_slurm_api):
    """Test to print per sample jobid yaml"""
    # GIVEN a slurm api, a job name and a command
    print_yaml=real_slurm_api.print_submitted_jobs(dry_run=True)
    
