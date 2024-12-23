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

# Fetch Patient Data

def fetch_data(fetch_method: Callable, patient_id: Optional[str] = None, variant_id: Optional[str] = None) -> Any:
    if patient_id and variant_id:
        return fetch_method(patient_id, variant_id)
    elif patient_id:
        return fetch_method(patient_id)
    else:
        return fetch_method()

@router.get("/snp_research")
def get_snp_research(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return fetch_data(genome_browser.fetch_all_snp_pairs, patient_id, variant_id)

@router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return fetch_data(genome_browser.fetch_patient_data_genotypes, patient_id, variant_id)

@router.get("/patient_genome_data/expanded")
def get_patient_genome_data_expanded(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return fetch_data(genome_browser.fetch_patient_data_expanded, patient_id, variant_id)

@router.get("/full_report")
def get_full_report(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return fetch_data(genome_browser.fetch_full_report, patient_id, variant_id)
