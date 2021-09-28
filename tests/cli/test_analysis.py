"""Tests for base cli"""

from fluffy.cli import base
import sys

def test_analysis():
    """Test the version command"""
    # GIVEN a cli runner
    # WHEN running the version command
    config="tests/fixtures/config.json"
    sample="tests/fixtures/samplesheet.csv"

    sys.argv.append("--analyse")
    sys.argv.append("--dry_run")
    sys.argv+=["-c",config]
    sys.argv+=["-o","tmp/test_fluffy"]
    sys.argv+=["-p","tests/fixtures/project"]
    sys.argv+=["-s",sample]

    results=base.base_command()

#test_version()
