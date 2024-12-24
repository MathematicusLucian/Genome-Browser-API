from repositories.patient_genome_repository import PatientGenomeRepository
from repositories.genome_research_repository import GenomeResearchRepository

class GenomeDatabaseManager:
    def __init__(self, db_path):
        self.genome_research_repository = GenomeResearchRepository(db_path)
        self.patient_genome_repository = PatientGenomeRepository(db_path)

    def close_connection(self):
        self.genome_research_repository.close_connection()
        self.patient_genome_repository.close_connection()

    def update_or_insert_snp_pair(self, snp_pair):
        self.genome_research_repository.update_or_insert_snp_pair(snp_pair)

    def save_snp_pairs_to_db(self, snp_df):
        self.genome_research_repository.save_snp_pairs_to_db(snp_df)

    def update_or_insert_patient(self, patient):
        self.patient_genome_repository.update_or_insert_patient(patient)

    def update_or_insert_patient_genome_data(self, patient_genome_data):
        self.patient_genome_repository.update_or_insert_patient_genome_data(patient_genome_data)

    def update_patient_and_genome_data(self, patient_df, patient_id, patient_name):
        self.patient_genome_repository.update_patient_and_genome_data(patient_df, patient_id, patient_name)

    def fetch_snp_pairs_data(self, offset=0, **kwargs):
        return self.genome_research_repository.fetch_snp_pairs_data(offset=offset, **kwargs)

    def fetch_genes_in_genome(self, offset=0, **kwargs):
        return self.genome_research_repository.fetch_genes_in_genome(offset=offset, **kwargs)

    def fetch_patients(self, offset=0, **kwargs):
        return self.patient_genome_repository.fetch_patients(offset=offset, **kwargs)

    def fetch_patient_genome_data(self, offset=0, **kwargs):
        return self.patient_genome_repository.fetch_patient_genome_data(offset=offset, **kwargs)
    
    def fetch_snp_pairs_data_by_genotype(self, offset=0, **kwargs):  
        return self.patient_genome_repository.fetch_snp_pairs_data_by_genotype(self, offset=offset, **kwargs)

    def fetch_patient_data_expanded(self, offset=0, **kwargs):
        return self.patient_genome_repository.fetch_patient_data_expanded(offset=offset, **kwargs)

    def fetch_full_report(self, offset=0, **kwargs):
        return self.patient_genome_repository.fetch_full_report(offset=offset, **kwargs)