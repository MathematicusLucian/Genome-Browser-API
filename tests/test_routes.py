import pytest
from fastapi.testclient import TestClient
from src.routes import router
from unittest.mock import patch, MagicMock

client = TestClient(router)

@pytest.fixture
def mock_genome_service():
    with patch('src.routes.GenomeService') as MockGenomeService:
        yield MockGenomeService.return_value

def test_load_genome_positive(mock_genome_service):
    mock_genome_service.load_genome_background.return_value = None
    response = client.post("/load_genome", params={"genome_file_name_with_path": "path/to/genome/file"})
    assert response.status_code == 200
    assert response.json() == {"message": "Genome loading commenced", "genome_file_name_with_path": "path/to/genome/file"}

def test_load_genome_negative(mock_genome_service):
    mock_genome_service.load_genome_background.side_effect = Exception("Load failed")
    response = client.post("/load_genome", params={"genome_file_name_with_path": "path/to/genome/file"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Load failed"}

def test_get_full_report_positive(mock_genome_service):
    mock_genome_service.fetch_patients.return_value = {"patients": []}
    response = client.get("/patients")
    assert response.status_code == 200
    assert response.json() == {"patients": []}

def test_get_full_report_negative(mock_genome_service):
    mock_genome_service.fetch_patients.side_effect = Exception("Fetch failed")
    response = client.get("/patients")
    assert response.status_code == 500
    assert response.json() == {"detail": "Fetch failed"}

def test_get_snp_research_positive(mock_genome_service):
    mock_genome_service.fetch_all_snp_pairs.return_value = {"snp_pairs": []}
    response = client.get("/snp_research", params={"variant_id": "rs123"})
    assert response.status_code == 200
    assert response.json() == {"snp_pairs": []}

def test_get_snp_research_negative(mock_genome_service):
    mock_genome_service.fetch_all_snp_pairs.side_effect = Exception("Fetch failed")
    response = client.get("/snp_research", params={"variant_id": "rs123"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Fetch failed"}

def test_get_list_of_chromosomes_from_ensembl_api_positive(mock_genome_service):
    mock_genome_service.fetch_chromosomes_from_ensembl.return_value = {"chromosomes": []}
    response = client.get("/fetch_chromosomes/ensembl")
    assert response.status_code == 200
    assert response.json() == {"chromosomes": []}

def test_get_list_of_chromosomes_from_ensembl_api_negative(mock_genome_service):
    mock_genome_service.fetch_chromosomes_from_ensembl.side_effect = Exception("Fetch failed")
    response = client.get("/fetch_chromosomes/ensembl")
    assert response.status_code == 500
    assert response.json() == {"detail": "Fetch failed"}

def test_get_list_of_chromosomes_from_gprofiler_api_positive(mock_genome_service):
    mock_genome_service.fetch_chromosomes_from_gprofiler.return_value = {"chromosomes": []}
    response = client.get("/fetch_chromosomes/gprofiler")
    assert response.status_code == 200
    assert response.json() == {"chromosomes": []}

def test_get_list_of_chromosomes_from_gprofiler_api_negative(mock_genome_service):
    mock_genome_service.fetch_chromosomes_from_gprofiler.side_effect = Exception("Fetch failed")
    response = client.get("/fetch_chromosomes/gprofiler")
    assert response.status_code == 500
    assert response.json() == {"detail": "Fetch failed"}

def test_get_from_gprofiler_api_gene_data_matching_variant_rsid_positive(mock_genome_service):
    mock_genome_service.fetch_gene_data_by_variant.return_value = {"gene_data": []}
    response = client.get("/fetch_gene_by_variant", params={"variant_id": "rs123"})
    assert response.status_code == 200
    assert response.json() == {"gene_data": []}

def test_get_from_gprofiler_api_gene_data_matching_variant_rsid_negative(mock_genome_service):
    mock_genome_service.fetch_gene_data_by_variant.side_effect = Exception("Fetch failed")
    response = client.get("/fetch_gene_by_variant", params={"variant_id": "rs123"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Fetch failed"}