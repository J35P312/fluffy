"""Tests for base cli"""
import logging
import sys

from click.testing import CliRunner

from fluffy.cli import base

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def test_version(caplog):
    """Test the version command"""
    caplog.set_level(logging.INFO, logger="base")
    # GIVEN a cli runner
    runner = CliRunner()
    # WHEN running the version command
    result = runner.invoke(base.base_command, ["--version"])
    assert "version" in result.output

    assert result.exit_code == 0
