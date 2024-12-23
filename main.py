import pandas as pd
import re
import os
from utils import load_file

class GenomeBrowser:
    def __init__(self, snp_pairs_file_name_with_path=None):
        self.genome_df = pd.DataFrame() | None
        self.snp_pairs_data = self.load_snp_pairs_data(snp_pairs_file_name_with_path)  

    def load_snp_pairs_data(self, snp_pairs_file_name_with_path):
        return load_file(snp_pairs_file_name_with_path)

    def load_genome(self, genome_file_name_with_path):
        self.genome_df = load_file(genome_file_name_with_path, names=["rsid","chromosome","position","genotype"])

    def retrieve_data_by_column(self, column_name, key_to_find):
        if self.genome_df is not None:
            if column_name in self.genome_df.columns:
                gene_variant = self.genome_df.loc[self.genome_df[column_name] == key_to_find] 
                if not gene_variant.empty:
                    return gene_variant
            else:
                print(f"No data found for {key_to_find} in column {column_name}.")
                return None
        else:
            print("No genome data loaded.")

if __name__ == "__main__":
    print("Genome Browser")
    base_path = os.getenv('PYTHONPATH', os.getcwd())
    snp_pairs_file_name_with_path = os.path.join(base_path, 'data/snp_pairs/snp_data.csv')
    genome_file_name_with_path = './data/genomes/genome_Lilly_Mendel_v4.txt'
    genome_browser = GenomeBrowser(snp_pairs_file_name_with_path)
    genome_browser.load_genome(genome_file_name_with_path)
    column_name = 'rsid'
    gene_variant = genome_browser.retrieve_data_by_column(column_name, 'rs1050828') 
    print(gene_variant)