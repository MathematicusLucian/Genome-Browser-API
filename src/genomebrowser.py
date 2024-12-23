import pandas as pd
import re
from utils import load_file

class GenomeBrowser:
    def __init__(self, snp_pairs_file_name_with_path=None):
        self.patient_genome_df = pd.DataFrame() | None
        if snp_pairs_file_name_with_path is not None:
            self.snp_pairs_data = self.load_snp_pairs_data(snp_pairs_file_name_with_path)  

    def load_snp_pairs_data(self, snp_pairs_file_name_with_path):
        return load_file(snp_pairs_file_name_with_path)

    def load_genome(self, genome_file_name_with_path):
        self.patient_genome_df = load_file(genome_file_name_with_path, names=["rsid","chromosome","position","genotype"])

    def retrieve_data_by_column(self, column_name, key_to_find):
        if self.patient_genome_df is not None:
            if column_name in self.patient_genome_df.columns:
                gene_variant = self.patient_genome_df.loc[self.patient_genome_df[column_name] == key_to_find] 
                if not gene_variant.empty:
                    return gene_variant
            else:
                print(f"No data found for {key_to_find} in column {column_name}.")
                return None
        else:
            print("No genome data loaded.")

    def fetch_gene_variant(self, key_to_find):
        column_name = 'rsid'
        gene_variant = self.retrieve_data_by_column(column_name, key_to_find) 
        if gene_variant is not None:
            return gene_variant
        else:
            print(f"No gene variant found for {column_name} with key '{key_to_find}'.")