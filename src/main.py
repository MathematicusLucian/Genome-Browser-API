import os
from dotenv import load_dotenv
import pandas as pd
from genomebrowser import GenomeBrowser

def setup():
    load_dotenv()
    snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
    genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')
    genome_browser = GenomeBrowser(snp_pairs_file_name_with_path)
    genome_browser.load_genome(genome_file_name_with_path)
    return genome_browser

if __name__ == "__main__":
    genome_browser = setup()
    
    gene_variant = genome_browser.fetch_gene_variant('rs1050828') 
    print(gene_variant)