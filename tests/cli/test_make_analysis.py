"""Tests for the make analysis command"""

from click.testing import CliRunner

from fluffy.cli.make_analysis import analyse


def test_analyse_cmd(base_context):
    """Test to run the analysis command"""
    # GIVEN a cli runnner
    runner = CliRunner()
    # WHEN running the analyse command
    result = runner.invoke(analyse, ["--skip-preface"], obj=base_context)
    # THEN assert that the command exits without problems
    assert result.exit_code == 0
