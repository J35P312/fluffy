"""
fluffy.__main__
~~~~~~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``fluffy`` (if installed)
or ``python -m fluffy`` (no install required).
"""
import sys

from fluffy.cli.base import base_command

if __name__ == "__main__":
    # exit using whatever exit code the CLI returned
    sys.exit(base_command())
