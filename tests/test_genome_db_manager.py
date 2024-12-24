import os
import sys
from venv import logger
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import pandas as pd  
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
from genome_db_manager import GenomeDatabase

@pytest.fixture
def genome_db():
    db = GenomeDatabase()
    db.create_tables()
    yield db
    db.close_connection()

def fetch_all(result):
    if isinstance(result, list):
        return result
    return result.fetchall()

def fetch_one(result):
    if isinstance(result, list):
        return result[0] if result else None
    return result.fetchone()

def test_create_tables(genome_db):
    result = genome_db.sql_worker.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in fetch_all(result)]
    assert "snp_pairs" in tables
    assert "patients" in tables
    assert "patient_genome_data" in tables
    
def test_update_or_insert_snp_pair(genome_db):
    genome_db.update_or_insert_snp_pair("rs1234(A;A)", 1.0, 0.5, "note", "rs1234", "A", "A")
    result = genome_db.sql_worker.execute("SELECT * FROM snp_pairs WHERE rsid='rs1234';")
    result = fetch_one(result)
    assert result is not None
    assert result[0] == "rs1234(A;A)"
    assert result[1] == 1.0
    assert result[2] == 0.5
    assert result[3] == "note"
    assert result[4] == "rs1234"
    assert result[5] == "A"
    assert result[6] == "A"

def test_save_snp_pairs_to_db(genome_db):
    genome_db.sql_worker.execute("DELETE FROM snp_pairs;")
    snp_df = pd.DataFrame({
        "rsid_genotypes": ["rs1234(A;A)", "rs5678(G;G)"],
        "magnitude": [1.0, 2.0],
        "risk": [0.5, 1.5],
        "notes": ["note1", "note2"],
        "rsid": ["rs1234", "rs5678"],
        "allele1": ["A", "G"],
        "allele2": ["A", "G"]
    })
    genome_db.save_snp_pairs_to_db(snp_df)
    result = genome_db.sql_worker.execute("SELECT * FROM snp_pairs;")
    result = fetch_all(result)
    assert len(result) == 2

def test_update_or_insert_patient(genome_db):
    genome_db.update_or_insert_patient("patient1", "John Doe")
    result = genome_db.sql_worker.execute("SELECT * FROM patients WHERE patient_id='patient1';")
    result = fetch_one(result)
    assert result is not None
    assert result[0] == "patient1"
    assert result[1] == "John Doe"

def test_update_or_insert_patient_genome_data(genome_db):
    genome_db.sql_worker.execute("DELETE FROM patients;DELETE FROM patient_genome_data;")
    genome_db.update_or_insert_patient("patient1", "John Doe")
    genome_db.update_or_insert_patient_genome_data("rs1234", "patient1", "1", 12345, "AA")
    result = genome_db.sql_worker.execute("SELECT * FROM patient_genome_data WHERE rsid='rs1234';")
    result = fetch_one(result)
    assert result is not None
    assert result[1] == "rs1234"
    assert result[2] == "patient1"
    assert result[3] == "1"
    assert result[4] == 12345
    assert result[5] == "AA"

def test_update_patient_and_genome_data(genome_db):
    patient_df = pd.DataFrame({
        "rsid": ["rs1234", "rs5678"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })
    genome_db.update_patient_and_genome_data(patient_df, "patient1", "John Doe")
    result = genome_db.sql_worker.execute("SELECT * FROM patients WHERE patient_id='patient1';")
    result = fetch_one(result)
    assert result is not None
    assert result[0] == "patient1"
    assert result[1] == "John Doe"
    result = genome_db.sql_worker.execute("SELECT * FROM patient_genome_data WHERE patient_id='patient1';")
    result = fetch_all(result)
    assert len(result) == 2

def test_fetch_joined_patient_data(genome_db):
    genome_db.sql_worker.execute("DELETE FROM snp_pairs;")
    snp_df = pd.DataFrame({
        "rsid_genotypes": ["rs1234(A;A)", "rs5678(G;G)"],
        "magnitude": [1.0, 2.0],
        "risk": [0.5, 1.5],
        "notes": ["note1", "note2"],
        "rsid": ["rs1234", "rs5678"],
        "allele1": ["A", "G"],
        "allele2": ["A", "G"]
    })
    genome_db.save_snp_pairs_to_db(snp_df) 
    result = genome_db.fetch_snp_pairs_data()
    result = fetch_all(result)
    assert len(result) == 2
    assert result[0][0] == "rs1234(A;A)"
    assert result[0][3] == "note1"
    assert result[0][4] == "rs1234"
    assert result[1][3] == "note2"

def test_fetch_joined_patient_data(genome_db):
    patient_df = pd.DataFrame({
        "rsid": ["rs1234", "rs5678"],
        "chromosome": ["1", "2"],
        "position": [12345, 67890],
        "genotype": ["AA", "GG"]
    })
    genome_db.update_patient_and_genome_data(patient_df, "patient1", "John Doe")
    result = genome_db.fetch_joined_patient_data()
    result = fetch_all(result)
    assert len(result) == 2
    assert result[0][0] == "patient1"
    assert result[0][1] == "John Doe"
    assert result[0][2] == "rs1234"
    assert result[1][2] == "rs5678"