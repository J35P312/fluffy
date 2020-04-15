"""Tests for the config module"""

from pathlib import Path

import pytest

from fluffy import config


def test_file_exists():
    """Test if a file exists"""
    # GIVEN an existing file
    infile = Path(__file__)
    # WHEN checking if the file exists
    res = config.file_exists(infile)
    # THEN assert the result was True
    assert res is True


def test_file_exists_non_existing():
    """Test if a non existing file exists"""
    # GIVEN a non existing file
    infile = Path("non_existing")
    # WHEN checking if the file exists
    # THEN assert an exception was raised
    with pytest.raises(FileNotFoundError):
        config.file_exists(infile)


def test_get_configs(config_path):
    """Test if to parse a config file"""
    # GIVEN a config file
    # WHEN fetching the configs
    res = config.get_configs(config_path)
    # THEN assert the result is a populated dictionary
    assert res
    assert isinstance(res, dict)


def test_check_configs(configs):
    """Test to check a config file"""
    # GIVEN a config file
    # WHEN checking the configs
    config.check_configs(configs)
    # THEN assert that the function exits without exceptions
    assert True
