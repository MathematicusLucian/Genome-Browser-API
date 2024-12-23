import logging
from venv import logger
import pandas as pd
import re
from utils import load_file

def load_data(filename_with_path, names, straight=False):
    if(filename_with_path is not None):
        return load_file(filename_with_path, names, straight)
    else:
        return pd.DataFrame()
    
class GenomeBrowser(object):
    patient_genome_df = pd.DataFrame() | None
    snp_pairs_df = pd.DataFrame() | None

    def __init__(self, snp_pairs_file_name_with_path=None):
        if snp_pairs_file_name_with_path is not None:
            self.snp_pairs_df = self.load_snp_pairs_df(snp_pairs_file_name_with_path)  
 
    def extract_genotype_info(self, df):
        df['RSID'] = df['RSID_Genotypes'].str.extract(r'(Rs\d+)\(')
        df['Allele1'] = df['RSID_Genotypes'].str.extract(r'\(([^;]+)')
        df['Allele2'] = df['RSID_Genotypes'].str.extract(r';([^)]+)\)')
        return df

    def load_snp_pairs_df(self, snp_pairs_file_name_with_path):
        index_column_name = 'rsid' 
        snp_df = load_data(snp_pairs_file_name_with_path, names=None, straight=True)
        pattern = 'Rs'
        mask = snp_df['RSID_Genotypes'].str.startswith(pattern)
        snp_df = snp_df[mask]
        snp_df = self.extract_genotype_info(snp_df)
        new_cols = ['rsid_genotypes', 'magnitude', 'risk', 'notes', 'rsid', 'allele1', 'allele2']
        snp_df.columns = new_cols
        snp_df[index_column_name] = snp_df[index_column_name].map(lambda x : x.lower())
        if snp_df is not None:
            return snp_df
        else:
            raise TypeError("No SNP data loaded.")

    def load_genome(self, genome_file_name_with_path):
        self.patient_genome_df = load_data(genome_file_name_with_path, names=["rsid","chromosome","position","genotype"])
        return self.patient_genome_df.size

    def retrieve_data_by_column(self, df, column_name, key_to_find):
        if df is not None:
            if column_name in df.columns:
                gene_variant = df.loc[df[column_name] == key_to_find] 
                if not gene_variant.empty:
                    return gene_variant
            else:
                raise TypeError(f"No data found for {key_to_find} in column {column_name}.")
        else:
            raise TypeError("No genome data loaded.")

    def fetch_gene_variant_patient_details(self, key_to_find):
        column_name = 'rsid'
        gene_variant_patient_details = self.retrieve_data_by_column(self.patient_genome_df, column_name, key_to_find) 
        if gene_variant_patient_details is not None:
            return gene_variant_patient_details
        else:
            raise TypeError(f"No gene variant found for {column_name} with key '{key_to_find}'.")

    def fetch_gene_variant_research(self, key_to_find):
        column_name = 'rsid'
        gene_variant_research = self.retrieve_data_by_column(self.snp_pairs_df, column_name, key_to_find) 
        if gene_variant_research is not None:
            return gene_variant_research
        else:
            raise TypeError(f"No gene variant found for {column_name} with key '{key_to_find}'.")
    
    def fetch_full_report_by_gene_variant(self, key_to_find):
        patient_df = self.fetch_gene_variant_patient_details(key_to_find) 
        snp_df = self.fetch_gene_variant_research(key_to_find)  
        full_report_gene_variant_df = pd.merge(patient_df, snp_df, on='rsid', how='inner')
        snp_pairs_genotype = full_report_gene_variant_df.allele1 + full_report_gene_variant_df.allele2
        matching_merged_df = full_report_gene_variant_df[(full_report_gene_variant_df['genotype'] == snp_pairs_genotype) | (full_report_gene_variant_df['genotype'].str[::-1] == snp_pairs_genotype)]
        if matching_merged_df is not None:
            matching_merged_df.head(5)
            return matching_merged_df
        else:
            raise TypeError(f"No gene variant found for {key_to_find}.")

    def fetch_full_report(self):
        patient_df = self.snp_pairs_df
        snp_df = self.patient_genome_df
        full_report_gene_variant_df = pd.merge(patient_df, snp_df, on='rsid', how='inner')
        snp_pairs_genotype = full_report_gene_variant_df.allele1 + full_report_gene_variant_df.allele2
        matching_merged_df = full_report_gene_variant_df[(full_report_gene_variant_df['genotype'] == snp_pairs_genotype) | (full_report_gene_variant_df['genotype'].str[::-1] == snp_pairs_genotype)]
        pd.set_option('display.max_rows', 1000)
        if matching_merged_df is not None:
            matching_merged_df.head(5)
            return matching_merged_df
        else:
            raise TypeError("No gene variants found.")