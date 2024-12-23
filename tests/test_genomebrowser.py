import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import pandas as pd  
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from genomebrowser import GenomeBrowser

# Mock the load_file method to provide the mock dataframe
def test_retrieve_data_by_column_positive():
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        result = gb.retrieve_data_by_column("rsid", "rs1050828")
        assert not result.empty
        assert result.iloc[0]["rsid"] == "rs1050828"

# Positive case: another valid column and key
def test_retrieve_data_by_column_positive_another_key():
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        result = gb.retrieve_data_by_column("rsid", "rs1234567")
        assert not result.empty
        assert result.iloc[0]["rsid"] == "rs1234567" 

# Negative case: column not found
def test_retrieve_data_by_column_negative_column_not_found():
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        with pytest.raises(TypeError):
            gb.retrieve_data_by_column("nonexistent_column", "rs1050828") 

# Negative case: key not found
def test_retrieve_data_by_column_negative_key_not_found(): 
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        result = gb.retrieve_data_by_column("rsid", "rs9999999") 
        assert result is None

# Negative case: no genome data loaded
def test_retrieve_data_by_column_no_genome_data():
    gb = GenomeBrowser() 
    with pytest.raises(TypeError):
        gb.retrieve_data_by_column("rsid", "rs1050828")  

# Negative case: invalid column type
def test_retrieve_data_by_column_invalid_column_type(): 
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        with pytest.raises(TypeError):
            gb.retrieve_data_by_column(123, "rs1050828")

# Positive case: valid fetch_gene_variant
def test_fetch_gene_variant_positive(): 
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        result = gb.fetch_gene_variant("rs1050828")
        assert not result.empty
        assert result.iloc[0]["rsid"] == "rs1050828" 

# Negative case: fetch_gene_variant key not found. xception handling: invalid key type
def test_fetch_gene_variant_negative_key_not_found(): 
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None)
        with pytest.raises(TypeError):
            gb.fetch_gene_variant("rs9999999")

# Negative case: fetch_gene_variant key not found
def test_fetch_gene_variant_invalid_key_type(): 
    with patch('genomebrowser.GenomeBrowser.patient_genome_df', pd.DataFrame({
        "rsid": ["rs1050828", "rs1234567"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })): # Directly set the dataframe
        gb = GenomeBrowser(None) 
        with pytest.raises(TypeError):
            gb.fetch_gene_variant(12345)