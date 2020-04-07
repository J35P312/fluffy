"""Utils for fluffy commands"""

import pathlib


def get_outprefix(out: pathlib.Path, sample_id: str) -> str:
    """Create a path to a out directory"""

    return out / sample_id / sample_id
