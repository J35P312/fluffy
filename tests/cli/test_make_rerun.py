"""Tests for the make rerun command"""

from click.testing import CliRunner

from fluffy.cli.make_rerun import rerun


def test_rerun_cmd(base_context):
    """Test to run the analysis command"""
    # GIVEN a cli runnner
    runner = CliRunner()
    # WHEN running the analyse command
    result = runner.invoke(rerun,["--dry-run"], obj=base_context)
    # THEN assert that the command exits without problems
    assert result.exit_code == 0
