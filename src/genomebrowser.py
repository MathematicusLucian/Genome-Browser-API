import logging
from venv import logger
from annotated_types import T
import pandas as pd
import uuid
import genomedatabase
from utils import load_file, check_if_default

def load_data(filename_with_path, names, straight=False):
    if(filename_with_path is not None):
        return load_file(filename_with_path, names, straight)
    else:
        return pd.DataFrame()

class GenomeBrowser(object):
    patient_genome_df = pd.DataFrame() | None
    snp_pairs_df = pd.DataFrame() | None
    genome_database = genomedatabase.GenomeDatabase()  

    def __init__(self, snp_pairs_file_name_with_path=None, genome_database=None):
        self.genome_database = genome_database
        self.genome_database.create_tables()
        if snp_pairs_file_name_with_path is not None:
            self.load_snp_pairs_df(snp_pairs_file_name_with_path)
 
    def extract_genotype_info(self, df):
        df['RSID'] = df['RSID_Genotypes'].str.extract(r'(Rs\d+)\(')
        df['Allele1'] = df['RSID_Genotypes'].str.extract(r'\(([^;]+)')
        df['Allele2'] = df['RSID_Genotypes'].str.extract(r';([^)]+)\)')
        return df

    def retrieve_data_by_column(self, df, column_name, key_to_find):
        if df is not None:
            if column_name in df.columns:
                data = df.loc[df[column_name] == key_to_find] 
                if not data.empty:
                    return data
            else:
                raise TypeError(f"No data found for {key_to_find} in column {column_name}.")
        else:
            raise TypeError(f"No {key_to_find} data loaded.")

    # Patient SNP Pairs Matches
    
    # SNP Pairs data

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
        if snp_df is not None and self.genome_database is not None:
            self.genome_database.save_snp_pairs_to_db(snp_df) 
            self.snp_pairs_df = snp_df
        else:
            raise TypeError("No SNP data loaded.")
    
    def fetch_all_snp_pairs(self): 
        column_name = 'rsid'
        gene_variant_research = self.genome_database.fetch_snp_pairs_data(offset=0) 
        if gene_variant_research is not None:
            return gene_variant_research
        else:
            raise TypeError(f"No gene variant found for {column_name}.")


    def fetch_all_snp_pairs(self, patient_id: str): 
        column_name = 'rsid'
        gene_variant_research = self.genome_database.fetch_snp_pairs_data(patient_id, offset=0) 
        if gene_variant_research is not None:
            return gene_variant_research
        else:
            raise TypeError(f"No gene variant found for {column_name}.")


    def fetch_all_snp_pairs(self, patient_id: str, variant_id: str): 
        column_name = 'rsid'
        rsid = check_if_default(variant_id)
        gene_variant_research = self.genome_database.fetch_snp_pairs_data(patient_id, rsid, offset=0) 
        if gene_variant_research is not None:
            return gene_variant_research
        else:
            raise TypeError(f"No gene variant found for {column_name} with key '{rsid}'.")
        
    # Patient Genome: /patient 

    def load_genome(self, genome_file_name_with_path: str):
        self.patient_genome_df = load_data(genome_file_name_with_path, names=["rsid", "chromosome", "position", "genotype"])
        if self.patient_genome_df is not None and self.genome_database is not None:
            self.genome_database.update_patient_and_genome_data(self.patient_genome_df, str(uuid.uuid4()), genome_file_name_with_path)
        return self.patient_genome_df.size

    # List of All Patients

    def fetch_patients(self):
        patients = self.genome_database.fetch_patients_list(offset=0)
        if patients is not None:
            return patients
        else:
            raise TypeError("No patients - load patient data.")

    # Individual Patient Data

    def fetch_patient_data_genotypes(self): 
        column_name = 'rsid'
        patients_genome_data_all = self.genome_database.fetch_patients_genome_data_all(offset=0)
        if patients_genome_data_all is not None:
            return patients_genome_data_all
        else:
            raise TypeError(f"No fetch_patient_data_genotypes found for {column_name}.")


    def fetch_patient_data_genotypes(self, patient_id: str): 
        column_name = 'rsid'
        patients_genome_data_all = self.genome_database.fetch_patients_genome_data_all(patient_id, offset=0)
        if patients_genome_data_all is not None:
            return patients_genome_data_all
        else:
            raise TypeError(f"No fetch_patient_data_genotypes found for {column_name}.")


    def fetch_patient_data_genotypes(self, patient_id: str, variant_id: str): 
        column_name = 'rsid'
        rsid = check_if_default(variant_id)
        patients_genome_data_all = self.genome_database.fetch_patients_genome_data_all(patient_id, rsid, offset=0)
        if patients_genome_data_all is not None:
            return patients_genome_data_all
        else:
            raise TypeError(f"No fetch_patient_data_genotypes found for {column_name} with key '{rsid}'.")
        
    # Individual Patient Data Expanded (Featuring Their Genotypes)
    
    def fetch_patient_data_expanded(self): 
        gene_variant_patient_details = self.genome_database.fetch_joined_patient_data(offset=0) 
        if gene_variant_patient_details is not None:
            return gene_variant_patient_details
        else:
            raise TypeError("No patients data found.")
    
    def fetch_patient_data_expanded(self, patient_id: str): 
        column_name = 'rsid' 
        gene_variant_patient_details = self.genome_database.fetch_joined_patient_data_by_rsid(patient_id, offset=0) 
        if gene_variant_patient_details is not None:
            return gene_variant_patient_details
        else:
            raise TypeError(f"No patients data found for {column_name} with patient_id '{patient_id}'.")
    
    def fetch_patient_data_expanded(self, patient_id: str, variant_id: str): 
        column_name = 'rsid'
        rsid = check_if_default(variant_id)
        gene_variant_patient_details = self.genome_database.fetch_joined_patient_data_by_rsid(patient_id, rsid, offset=0) 
        if gene_variant_patient_details is not None:
            return gene_variant_patient_details
        else:
            raise TypeError(f"No patients data found for {column_name} with key '{rsid}'.")

    # Patient Data plus SNP Matches

    def fetch_full_report(self): 
        patient_data_as_list = self.genome_database.fetch_joined_patient_data(offset=0)
        if patient_data_as_list is not None:
            return patient_data_as_list
        else:
            raise TypeError("No data found.")

    def fetch_full_report(self, patient_id: str): 
        patient_data_as_list = self.genome_database.fetch_joined_patient_data(patient_id, offset=0)
        if patient_data_as_list is not None:
            return patient_data_as_list
        else:
            raise TypeError("No data found.")


    def fetch_full_report(self, patient_id: str, variant_id: str): 
        column_name = 'rsid'
        rsid = check_if_default(variant_id)  
        patient_data_as_list = self.genome_database.fetch_joined_patient_data(patient_id, rsid, offset=0) 
        if patient_data_as_list is not None:
            return patient_data_as_list
        else:
            raise TypeError(f"No patients data found for {column_name} with key '{rsid}'.")