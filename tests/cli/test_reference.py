"""Tests for base cli"""

from fluffy.cli import base
import sys

def test_reference(config_path,out_dir):
    """Test the version command"""
    # GIVEN a cli runner
    # WHEN running the version command
    sample="tests/fixtures/samplesheet.csv"

    sys.argv.append("--reference")
    sys.argv.append("--dry_run")
    sys.argv+=["-c",str(config_path)]
    sys.argv+=["-o",str(out_dir)]
    sys.argv+=["-p","tests/fixtures/project"]
    sys.argv+=["-s",sample]

    results=base.base_command()

#test_version()
