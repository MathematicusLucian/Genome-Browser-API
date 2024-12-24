import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.controllers.genome_controller import router
from src.services.genome_service import GenomeService

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