import os
from dotenv import load_dotenv
import pandas as pd
from genomebrowser import GenomeBrowser

load_dotenv()
snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')

def setup():
    return GenomeBrowser(snp_pairs_file_name_with_path)

if __name__ == "__main__":
    # Load a genome browser object (featuring SNP pairs data)
    genome_browser = setup()

    #  Add patient data to the genome browser object 
    genome_browser.load_genome(genome_file_name_with_path)
    
    fetch_gene_variant_patient_details = genome_browser.fetch_gene_variant_patient_details('Rs10516809') 
    print(f'Patient: {fetch_gene_variant_patient_details}')
    fetch_gene_variant_research = genome_browser.fetch_gene_variant_research('Rs10516809') 
    print(f'Research: {fetch_gene_variant_research}')