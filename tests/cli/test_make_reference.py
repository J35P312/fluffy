"""Tests for the make reference command"""

from click.testing import CliRunner

from fluffy.cli.make_reference import reference


def test_reference_cmd(base_context):
    """Test to run the analysis command"""
    # GIVEN a cli runnner
    runner = CliRunner()
    # WHEN running the analyse command
    result = runner.invoke(reference, obj=base_context)
    # THEN assert that the command exits without problems
    assert result.exit_code == 0
