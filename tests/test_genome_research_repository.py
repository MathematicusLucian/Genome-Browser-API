import pytest
from unittest.mock import patch, MagicMock
from repositories.genome_research_repository import GenomeResearchRepository

@pytest.fixture
def genome_repository():
    return GenomeResearchRepository(db_path=":memory:")

def test_save_snp_pairs_to_db_positive(genome_repository):
    snp_df = MagicMock()
    with patch.object(genome_repository, 'execute_query', return_value=True) as mock_method:
        result = genome_repository.save_snp_pairs_to_db(snp_df)
        mock_method.assert_called_once()
        assert result is True

def test_save_snp_pairs_to_db_negative(genome_repository):
    snp_df = MagicMock()
    with patch.object(genome_repository, 'execute_query', side_effect=Exception("DB Error")) as mock_method:
        result = genome_repository.save_snp_pairs_to_db(snp_df)
        mock_method.assert_called_once()
        assert result is False

def test_update_or_insert_snp_pair_positive(genome_repository):
    snp_pair = {"snp1": "rs123", "snp2": "rs456"}
    with patch.object(genome_repository, 'execute_query', return_value=True) as mock_method:
        result = genome_repository.update_or_insert_snp_pair(snp_pair)
        mock_method.assert_called_once()
        assert result is True

def test_update_or_insert_snp_pair_negative(genome_repository):
    snp_pair = {"snp1": "rs123", "snp2": "rs456"}
    with patch.object(genome_repository, 'execute_query', side_effect=Exception("DB Error")) as mock_method:
        result = genome_repository.update_or_insert_snp_pair(snp_pair)
        mock_method.assert_called_once()
        assert result is False

def test_fetch_snp_pairs_data_positive(genome_repository):
    with patch.object(genome_repository, 'execute_query', return_value=[{"snp1": "rs123", "snp2": "rs456"}]) as mock_method:
        result = genome_repository.fetch_snp_pairs_data()
        mock_method.assert_called_once()
        assert result == [{"snp1": "rs123", "snp2": "rs456"}]

def test_fetch_snp_pairs_data_negative(genome_repository):
    with patch.object(genome_repository, 'execute_query', side_effect=Exception("DB Error")) as mock_method:
        result = genome_repository.fetch_snp_pairs_data()
        mock_method.assert_called_once()
        assert result is None