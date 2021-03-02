"""Tests for samplesheet.py"""

from fluffy import samplesheet


def test_get_separator_space():
    """Test to get a separator"""
    # GIVEN a line with spaces
    line = "one two three"
    # WHEN getting the separator
    sep = samplesheet.get_separator(line)
    # THEN assert space is returned
    assert sep == " "


def test_get_separator_csv():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one,two,three"
    # WHEN getting the separator
    sep = samplesheet.get_separator(line)
    # THEN assert comma is returned
    assert sep == ","


def test_get_separator_tab():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one\ttwo\tthree"
    # WHEN getting the separator
    sep = samplesheet.get_separator(line)
    # THEN assert None is returned
    assert sep is None


def test_get_separator_semi():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one;two;three"
    # WHEN getting the separator
    sep = samplesheet.get_separator(line)
    # THEN assert None is returned
    assert sep is None


def test_get_separator_unknown():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one.two.three"
    # WHEN getting the separator
    sep = samplesheet.get_separator(line)
    # THEN assert None is returned
    assert sep is None


def test_get_sample_col():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one two SampleID"
    # WHEN finding the sample col
    col_nr = samplesheet.get_sample_col(line.split(" "))
    # THEN assert correct col nr is returned
    assert col_nr == 2

def test_get_sample_name():
    """Test to get a separator"""
    # GIVEN a line with commas as delimiter
    line = "one two SampleName"
    # WHEN finding the sample col
    col_nr = samplesheet.get_sample_Name_col(line.split(" "))
    # THEN assert correct col nr is returned
    assert col_nr == 2
