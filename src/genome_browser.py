import logging
import os
from dotenv import load_dotenv
import pandas as pd
import uuid 
from utils import load_file, check_if_default
from repositories.genome_repository import GenomeRepository

load_dotenv()

def load_data(filename_with_path, names, straight=False):
    if(filename_with_path is not None):
        return load_file(filename_with_path, names, straight)
    else:
        return pd.DataFrame()

class GenomeBrowser(object):
    patient_genome_df = pd.DataFrame() | None
    snp_pairs_df = pd.DataFrame() | None
    genome_repository = None
    default_genome_file_name_with_path = None

    def __init__(self, snp_pairs_file_name_with_path=None, default_genome_file_name_with_path=None, genome_repository=None):
        self.genome_repository = genome_repository
        self.default_genome_file_name_with_path = default_genome_file_name_with_path
        if snp_pairs_file_name_with_path is not None:
            self.load_snp_pairs_df(snp_pairs_file_name_with_path)
 
    def _extract_genotype_info(self, df):
        df['RSID'] = df['RSID_Genotypes'].str.extract(r'(Rs\d+)\(')
        df['Allele1'] = df['RSID_Genotypes'].str.extract(r'\(([^;]+)')
        df['Allele2'] = df['RSID_Genotypes'].str.extract(r';([^)]+)\)')
        return df

    def _generate_error_message(self, column_name, kwargs):
        error_message = f"No data found for {column_name}."
        if 'rsid' in kwargs:
            error_message += f" with key '{kwargs['rsid']}'."
        if 'patient_id' in kwargs:
            error_message += f" for patient_id '{kwargs['patient_id']}'."
            raise TypeError(error_message)

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
        snp_df = self._extract_genotype_info(snp_df)
        new_cols = ['rsid_genotypes', 'magnitude', 'risk', 'notes', 'rsid', 'allele1', 'allele2']
        snp_df.columns = new_cols
        snp_df[index_column_name] = snp_df[index_column_name].map(lambda x : x.lower())
        if snp_df is not None and self.genome_repository is not None:
            self.genome_repository.save_snp_pairs_to_db(snp_df) 
            self.snp_pairs_df = snp_df
        else:
            raise TypeError("No SNP data loaded.")
    
    def fetch_all_snp_pairs(self, **kwargs): 
        column_name = 'rsid'
        if 'offset' not in kwargs: kwargs['offset'] = 0
        kwargs['rsid'] = check_if_default(kwargs.get('variant_id')) if kwargs.get('variant_id') else None
        gene_variant_research = self.genome_repository.fetch_snp_pairs_data(**kwargs)
        if gene_variant_research is not None:
            return gene_variant_research
        else:
            self._generate_error_message(column_name, kwargs)
        
    # Patient Genome: /patient 

    def load_genome(self, genome_file_name_with_path: str):
        if(genome_file_name_with_path == "default"):
            genome_file_name_with_path = self.default_genome_file_name_with_path
        self.patient_genome_df = load_data(genome_file_name_with_path, names=["rsid", "chromosome", "position", "genotype"])
        if self.patient_genome_df is not None and self.genome_repository is not None:
            self.genome_repository.update_patient_and_genome_data(self.patient_genome_df, str(uuid.uuid4()), genome_file_name_with_path)
        return self.patient_genome_df.size

    # Individual Patient Profiles 

    def fetch_patients(self):
        patients = self.genome_repository.fetch_patients_list(offset=0)
        if patients is not None:
            return patients
        else:
            raise TypeError("No patients - load patient data.")

    def fetch_patient_profile(self, **kwargs): 
        column_name = 'rsid'  
        if 'offset' not in kwargs: kwargs['offset'] = 0 
        patients_genome_data_all = self.genome_repository.fetch_patient_profile(**kwargs)
        if patients_genome_data_all is not None:
            return patients_genome_data_all
        else:         
            self._generate_error_message(column_name, kwargs) 

    # Individual Patient Genotypes 
    
    def fetch_patient_genome_data(self, **kwargs): 
        column_name = 'rsid'  
        if 'offset' not in kwargs: kwargs['offset'] = 0
        kwargs['rsid'] = check_if_default(kwargs.get('variant_id')) if kwargs.get('variant_id') else None
        patients_genome_data_all = self.genome_repository.fetch_patient_genome_data(**kwargs)
        if patients_genome_data_all is not None:
            return patients_genome_data_all
        else:         
            self._generate_error_message(column_name, kwargs) 
        
    # Individual Patient Data Expanded (Featuring Their Genotypes) 
        
    def fetch_patient_data_expanded(self, **kwargs): 
        column_name = 'rsid'
        if 'offset' not in kwargs: kwargs['offset'] = 0
        kwargs['rsid'] = check_if_default(kwargs.get('variant_id')) if kwargs.get('variant_id') else None
        gene_variant_patient_details = self.genome_repository.fetch_patient_data_expanded(**kwargs)
        if gene_variant_patient_details is not None:
            return gene_variant_patient_details
        else:
            self._generate_error_message(column_name, kwargs) 

    # Patient Data plus SNP Matches

    def fetch_full_report(self, **kwargs): 
        column_name = 'rsid'
        if 'offset' not in kwargs: kwargs['offset'] = 0
        kwargs['rsid'] = check_if_default(kwargs.get('variant_id')) if kwargs.get('variant_id') else None
        patient_data_as_list = self.genome_repository.fetch_full_report(**kwargs)
        if patient_data_as_list is not None:
            return patient_data_as_list
        else:
            self._generate_error_message(column_name, kwargs)