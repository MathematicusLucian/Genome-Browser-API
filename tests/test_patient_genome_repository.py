import pytest
from unittest.mock import patch, MagicMock
from repositories.patient_genome_repository import PatientGenomeRepository

@pytest.fixture
def genome_repository():
    return PatientGenomeRepository(db_path=":memory:")

def test_update_or_insert_patient_positive(genome_repository):
    patient = {"id": 1, "name": "John Doe"}
    with patch.object(genome_repository, 'execute_query', return_value=True) as mock_method:
        result = genome_repository.update_or_insert_patient(patient)
        mock_method.assert_called_once()
        assert result is True

def test_update_or_insert_patient_negative(genome_repository):
    patient = {"id": 1, "name": "John Doe"}
    with patch.object(genome_repository, 'execute_query', side_effect=Exception("DB Error")) as mock_method:
        result = genome_repository.update_or_insert_patient(patient)
        mock_method.assert_called_once()
        assert result is False