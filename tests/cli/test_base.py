"""Tests for base cli"""

from click.testing import CliRunner

from fluffy.cli import base


def test_version():
    """Test the version command"""
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the version command
    result = runner.invoke(base.base_command, ["--version"])
    assert "version" in result.output

    assert result.exit_code == 0
