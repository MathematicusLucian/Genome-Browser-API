import os
from dotenv import load_dotenv
from typing import Any, Callable, Optional
from fastapi import APIRouter, Depends
from genomebrowser import GenomeBrowser
from genomedatabase import GenomeDatabase

load_dotenv()
snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
default_genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')
 
router = APIRouter()

genome_browser = GenomeBrowser(
    snp_pairs_file_name_with_path=snp_pairs_file_name_with_path,
    default_genome_file_name_with_path=default_genome_file_name_with_path,
    genome_database=GenomeDatabase()
) 

# root

@router.get("/")
def root():
    return {"Genome Browser API": "Welcome to Genome Browser API"} 

# Patient Genome: /patient

@router.post("/load_genome/{genome_file_name_with_path}")
def load_genome(genome_file_name_with_path: str):
    genome_browser.load_genome(genome_file_name_with_path) 
    return {"Genome Loaded": genome_file_name_with_path,
            "Number of Rows": genome_browser.patient_genome_df.size}

# List of All Patients
@router.get("/patients")
def get_full_report():
    full_report = genome_browser.fetch_patients()
    return {"Patient": full_report}

# Patient SNP Pairs Matches

@router.get("/snp_research")
def get_snp_research(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    if patient_id and variant_id:
        data = genome_browser.fetch_all_snp_pairs(patient_id, variant_id)
    elif patient_id:
        data = genome_browser.fetch_all_snp_pairs(patient_id)
    else:
        data = genome_browser.fetch_all_snp_pairs()
    return data

# Individual Patient Data

@router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    if patient_id and variant_id:
        data = genome_browser.fetch_patient_data_genotypes(patient_id, variant_id)
    elif patient_id:
        data = genome_browser.fetch_patient_data_genotypes(patient_id)
    else:
        data = genome_browser.fetch_patient_data_genotypes()
    return data  
        
# Individual Patient Data Expanded (Featuring Their Genotypes)

@router.get("/patient_genome_data/expanded")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    if patient_id and variant_id:
        data = genome_browser.fetch_patient_data_expanded(patient_id, variant_id)
    elif patient_id:
        data = genome_browser.fetch_patient_data_expanded(patient_id)
    else:
        data = genome_browser.fetch_patient_data_expanded()
    return data   

# Patient Data plus SNP Matches

@router.get("/full_report")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    if patient_id and variant_id:
        data = genome_browser.fetch_full_report(patient_id, variant_id)
    elif patient_id:
        data = genome_browser.fetch_full_report(patient_id)
    else:
        data = genome_browser.fetch_full_report()
    return data   