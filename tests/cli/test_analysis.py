"""Tests for base cli"""

from fluffy.cli import base
import sys

def test_analysis(config_path,out_dir):
    """Test the version command"""
    # GIVEN a cli runner
    # WHEN running the version command
    #print(str(config_path))
    #print(out_dir)

    sample="tests/fixtures/samplesheet.csv"   

    sys.argv.append("--analyse")
    sys.argv.append("--dry_run")
    sys.argv+=["-c",str(config_path)]
    sys.argv+=["-o",str(out_dir) ]
    sys.argv+=["-p","tests/fixtures/project"]
    sys.argv+=["-s",sample]

    results=base.base_command()

#test_version()
