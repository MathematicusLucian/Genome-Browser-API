from repositories.genome_repository import GenomeRepository

class GenomeDatabase:
    def __init__(self, db_path):
        self.repository = GenomeRepository(db_path)

    def close_connection(self):
        self.repository.close_connection()

    def update_or_insert_snp_pair(self, snp_pair):
        self.repository.update_or_insert_snp_pair(snp_pair)

    def save_snp_pairs_to_db(self, snp_df):
        self.repository.save_snp_pairs_to_db(snp_df)

    def update_or_insert_patient(self, patient):
        self.repository.update_or_insert_patient(patient)

    def update_or_insert_patient_genome_data(self, patient_genome_data):
        self.repository.update_or_insert_patient_genome_data(patient_genome_data)

    def update_patient_and_genome_data(self, patient_df, patient_id, patient_name):
        self.repository.update_patient_and_genome_data(patient_df, patient_id, patient_name)

    def fetch_snp_pairs_data(self, offset=0, **kwargs):
        return self.repository.fetch_snp_pairs_data(offset, **kwargs)

    def fetch_genes_in_genome(self, offset=0, **kwargs):
        return self.repository.fetch_genes_in_genome(offset, **kwargs)

    def fetch_patients_list(self, offset=0):
        return self.repository.fetch_patients_list(offset)

    def fetch_patient_profile(self, offset=0, **kwargs):
        return self.repository.fetch_patient_profile(offset, **kwargs)

    def fetch_patient_genome_data(self, offset=0, **kwargs):
        return self.repository.fetch_patient_genome_data(offset, **kwargs)