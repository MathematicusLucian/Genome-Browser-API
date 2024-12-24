from dotenv import load_dotenv
from typing import Any, Optional
from fastapi import APIRouter
from fastapi.params import Query
from fastapi.responses import JSONResponse
import threading  
from controllers.genome_controller import GenomeController

load_dotenv()

genome_router = APIRouter() 
genome_controller = GenomeController()

# Patient Genome: /patient

@genome_router.post("/load_genome")
def load_genome(genome_file_name_with_path: Optional[str] = Query(None)): 
    """
        Load a genome file in the background.
        
        - **genome_file_name_with_path**: Optional; The path to the genome file to be loaded.

        Returns:
        - **JSONResponse**: Indicating that genome loading has commenced and the path to the genome file.
    """
    return genome_controller.load_genome(genome_file_name_with_path)

# List of All Patients

@genome_router.get("/patients")
def fetch_patients():
    """
        Retrieve the full report of patients.

        - **full_report**: A JSON object containing the full report of patients.

        Returns:
        - **JSONResponse**: A response object containing the full report in JSON format.
    """
    return genome_controller.fetch_patients()

# General Human Genome

@genome_router.get("/snp_research")
def get_snp_research(variant_id: Optional[str] = None):
    """
        Retrieve SNP research data.

        - **variant_id**: An optional string representing the variant ID.

        Returns:
        - **JSONResponse**: Containing SNP research data.
    """
    return genome_controller.get_snp_research(variant_id)

# Chromosomes
@genome_router.get("/fetch_chromosomes/ensembl")
def get_list_of_chromosomes_from_ensembl_api(): 
    """
        Fetch the list of chromosomes from the Ensembl API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return genome_controller.get_list_of_chromosomes_from_ensembl_api()

@genome_router.get("/fetch_chromosomes/gprofiler")
def get_list_of_chromosomes_from_gprofiler_api(): 
    """
        Fetch the list of chromosomes from the g:Profiler API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return genome_controller.get_list_of_chromosomes_from_gprofiler_api()

@genome_router.get("/fetch_gene_by_variant")
def get_from_gprofiler_api_gene_data_matching_variant_rsid(variant_id: Optional[str] = None):
    """
        Fetch gene data matching a variant RSID from the g:Profiler API.

        - **variant_id**: Optional; The RSID of the variant to fetch gene data for. (The fallback is 'rs11734132'.")

        Returns:
        - **JSONResponse**: Containing the details of the gene matching the variant RSID.
    """
    return genome_controller.get_from_gprofiler_api_gene_data_matching_variant_rsid(variant_id)

# Fetch Patient Data

@genome_router.get("/patient_profile")
def get_patient_genome_data(patient_id: Optional[str] = None):
    """
        Retrieve genome data for a specific patient.

        - **patient_id**: An optional string representing the ID of the patient whose genome data is to be fetched.

        Returns:
        - **JSONResponse**: Containing the patient's genome data.
    """
    return genome_controller.get_patient_genome_data(patient_id)

@genome_router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve genome data for a specific patient and variant.

        - **patient_id**: The ID of the patient whose genome data is to be retrieved.
        - **variant_id**: The ID of the variant to filter the genome data.

        Returns:
        - **JSONResponse**: Containing the genome data.
    """
    return genome_controller.get_patient_genome_data(patient_id, variant_id)

@genome_router.get("/patient_genome_data/expanded")
def get_patient_genome_data_expanded(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve expanded genome data for a patient.

        - **patient_id**: An optional ID of the patient whose genome data is to be retrieved.
        - **variant_id**: An optional ID of the variant to filter the genome data.
    """
    return genome_controller.get_patient_genome_data_expanded(patient_id, variant_id)

@genome_router.get("/full_report")
def get_full_report(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve the full report for a specific patient and variant.

        - **patient_id**: Optional; The ID of the patient for whom the report is to be fetched.
        - **variant_id**: Optional; The ID of the variant for which the report is to be fetched.

        Returns:
        - **JSONResponse**: Containing the full report data.
    """
    return genome_controller.get_full_report(patient_id, variant_id)