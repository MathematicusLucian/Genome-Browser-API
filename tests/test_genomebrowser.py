import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import pandas as pd  
from unittest.mock import patch
from genomebrowser import GenomeBrowser
@pytest.fixture
def genome_browser():
    gb = GenomeBrowser(None)
    return gb

# Mock the load_file method to provide the mock dataframe
@patch.object(GenomeBrowser, 'load_genome', new_callable=pd.DataFrame)
def test_retrieve_data_by_column_positive(mock_load_genome, genome_browser):
    mock_load_genome.return_value = None  # Mock the load_file method to do nothing
    genome_browser.patient_genome_df = pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })  # Directly set the dataframe 
    result = genome_browser.retrieve_data_by_column("rsid", "rs1050828")
    assert not result.empty
    assert result.iloc[0]["rsid"] == "rs1050828"

# Positive case: another valid column and key
@patch.object(GenomeBrowser, 'load_genome', new_callable=pd.DataFrame)
def test_retrieve_data_by_column_positive_another_key(mock_load_genome, genome_browser):
    mock_load_genome.return_value = None  # Mock the load_file method to do nothing
    genome_browser.patient_genome_df = pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })  # Directly set the dataframe 
    result = genome_browser.retrieve_data_by_column("rsid", "rs1234567")
    assert not result.empty
    assert result.iloc[0]["rsid"] == "rs1234567"

# # Negative case: column not found
@patch.object(GenomeBrowser, 'load_genome', new_callable=pd.DataFrame)
def test_retrieve_data_by_column_negative_column_not_found(mock_load_genome, genome_browser):
    mock_load_genome.return_value = None  # Mock the load_file method to do nothing
    genome_browser.patient_genome_df = pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })  # Directly set the dataframe 
    result = genome_browser.retrieve_data_by_column("nonexistent_column", "rs1050828")
    assert result is None

# # Negative case: key not found
@patch.object(GenomeBrowser, 'load_genome', new_callable=pd.DataFrame)
def test_retrieve_data_by_column_negative_key_not_found(mock_load_genome, genome_browser):
    mock_load_genome.return_value = None  # Mock the load_file method to do nothing
    genome_browser.patient_genome_df = pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })  # Directly set the dataframe 
    result = genome_browser.retrieve_data_by_column("rsid", "rs9999999")
    assert result is None