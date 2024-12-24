import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.controllers.genome_controller import router
from src.services.genome_service import GenomeService

client = TestClient(router)

@pytest.fixture
def mock_genome_service():
    with patch.object(GenomeService, 'fetch_full_report') as mock_fetch_full_report, \
         patch.object(GenomeService, 'fetch_patients') as mock_fetch_patients, \
         patch.object(GenomeService, 'fetch_all_snp_pairs') as mock_fetch_all_snp_pairs, \
         patch.object(GenomeService, 'fetch_chromosomes_from_ensembl') as mock_fetch_chromosomes_from_ensembl, \
         patch.object(GenomeService, 'fetch_chromosomes_from_gprofiler') as mock_fetch_chromosomes_from_gprofiler, \
         patch.object(GenomeService, 'fetch_gene_data_by_variant') as mock_fetch_gene_data_by_variant, \
         patch.object(GenomeService, 'fetch_patient_profile') as mock_fetch_patient_profile, \
         patch.object(GenomeService, 'fetch_patient_genome_data') as mock_fetch_patient_genome_data, \
         patch.object(GenomeService, 'fetch_patient_data_expanded') as mock_fetch_patient_data_expanded, \
         patch.object(GenomeService, 'load_genome_background') as mock_load_genome_background:
        yield {
            'fetch_full_report': mock_fetch_full_report,
            'fetch_patients': mock_fetch_patients,
            'fetch_all_snp_pairs': mock_fetch_all_snp_pairs,
            'fetch_chromosomes_from_ensembl': mock_fetch_chromosomes_from_ensembl,
            'fetch_chromosomes_from_gprofiler': mock_fetch_chromosomes_from_gprofiler,
            'fetch_gene_data_by_variant': mock_fetch_gene_data_by_variant,
            'fetch_patient_profile': mock_fetch_patient_profile,
            'fetch_patient_genome_data': mock_fetch_patient_genome_data,
            'fetch_patient_data_expanded': mock_fetch_patient_data_expanded,
            'load_genome_background': mock_load_genome_background
        }

def test_load_genome(mock_genome_service):
    response = client.post("/load_genome?genome_file_name_with_path=test_path")
    assert response.status_code == 200
    assert response.json() == {"message": "Genome loading commenced", "genome_file_name_with_path": "test_path"}

def test_get_patients(mock_genome_service):
    mock_genome_service['fetch_patients'].return_value = {"patients": ["patient1", "patient2"]}
    response = client.get("/patients")
    assert response.status_code == 200
    assert response.json() == {"patients": ["patient1", "patient2"]}

def test_get_snp_research(mock_genome_service):
    mock_genome_service['fetch_all_snp_pairs'].return_value = {"snp_data": "mock_data"}
    response = client.get("/snp_research?variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"snp_data": "mock_data"}

def test_get_chromosomes_from_ensembl(mock_genome_service):
    mock_genome_service['fetch_chromosomes_from_ensembl'].return_value = {"chromosomes": ["chr1", "chr2"]}
    response = client.get("/fetch_chromosomes/ensembl")
    assert response.status_code == 200
    assert response.json() == {"chromosomes": ["chr1", "chr2"]}

def test_get_chromosomes_from_gprofiler(mock_genome_service):
    mock_genome_service['fetch_chromosomes_from_gprofiler'].return_value = {"chromosomes": ["chr1", "chr2"]}
    response = client.get("/fetch_chromosomes/gprofiler")
    assert response.status_code == 200
    assert response.json() == {"chromosomes": ["chr1", "chr2"]}

def test_get_gene_data_by_variant(mock_genome_service):
    mock_genome_service['fetch_gene_data_by_variant'].return_value = {"gene_data": "mock_data"}
    response = client.get("/fetch_gene_by_variant?variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"gene_data": "mock_data"}

def test_get_patient_profile(mock_genome_service):
    mock_genome_service['fetch_patient_profile'].return_value = {"patient_profile": "mock_data"}
    response = client.get("/patient_profile?patient_id=123")
    assert response.status_code == 200
    assert response.json() == {"patient_profile": "mock_data"}

def test_get_patient_genome_data(mock_genome_service):
    mock_genome_service['fetch_patient_genome_data'].return_value = {"genome_data": "mock_data"}
    response = client.get("/patient_genome_data?patient_id=123&variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"genome_data": "mock_data"}

def test_get_patient_genome_data_expanded(mock_genome_service):
    mock_genome_service['fetch_patient_data_expanded'].return_value = {"expanded_data": "mock_data"}
    response = client.get("/patient_genome_data/expanded?patient_id=123&variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"expanded_data": "mock_data"}

def test_get_full_report(mock_genome_service):
    mock_genome_service['fetch_full_report'].return_value = {"full_report": "mock_data"}
    response = client.get("/full_report?patient_id=123&variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"full_report": "mock_data"}

client = TestClient(router)

@pytest.fixture
def mock_fetch_full_report():
    with patch.object(GenomeService, 'fetch_full_report') as mock_method:
        yield mock_method

def test_get_full_report_valid_patient_and_variant(mock_fetch_full_report):
    mock_fetch_full_report.return_value = {"patient_id": "123", "variant_id": "rs123456", "data": "mock_data"}
    response = client.get("/full_report?patient_id=123&variant_id=rs123456")
    assert response.status_code == 200
    assert response.json() == {"patient_id": "123", "variant_id": "rs123456", "data": "mock_data"}

def test_get_full_report_valid_patient_no_variant(mock_fetch_full_report):
    mock_fetch_full_report.return_value = {"patient_id": "123", "data": "mock_data"}
    response = client.get("/full_report?patient_id=123")
    assert response.status_code == 200
    assert response.json() == {"patient_id": "123", "data": "mock_data"}

def test_get_full_report_invalid_patient(mock_fetch_full_report):
    mock_fetch_full_report.return_value = {"error": "Patient not found"}
    response = client.get("/full_report?patient_id=invalid")
    assert response.status_code == 404
    assert response.json() == {"error": "Patient not found"}

def test_get_full_report_invalid_variant(mock_fetch_full_report):
    mock_fetch_full_report.return_value = {"error": "Variant not found"}
    response = client.get("/full_report?patient_id=123&variant_id=invalid")
    assert response.status_code == 404
    assert response.json() == {"error": "Variant not found"}