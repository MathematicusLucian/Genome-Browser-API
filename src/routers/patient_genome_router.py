from dotenv import load_dotenv
from typing import Any, Optional
from fastapi import APIRouter
from fastapi.params import Query
from fastapi.responses import JSONResponse
import threading  
from controllers.genome_controller import GenomeController

load_dotenv()

patient_genome_router = APIRouter() 
genome_controller = GenomeController() 

# Patient Genome: /patient

@patient_genome_router.post("/load_patient_genome")
def load_genome(genome_file_name_with_path: Optional[str] = Query(None)): 
    """
        Load a genome file in the background.
        
        - **genome_file_name_with_path**: Optional; The path to the genome file to be loaded.

        Returns:
        - **JSONResponse**: Indicating that genome loading has commenced and the path to the genome file.
    """
    return genome_controller.load_genome(genome_file_name_with_path)

# Fetch Patient Data

@patient_genome_router.get("/patient_profile")
def get_patient_profiles(patient_id: Optional[str] = None):
    """
        Retrieve profiles data for patients, or a specific patient.

        - **patient_id**: An optional string representing the ID of the patient whose data is to be fetched.

        Returns:
        - **JSONResponse**: Containing the patient data in JSON format.
    """
    return genome_controller.get_patient_profile(patient_id)

@patient_genome_router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, rsid: Optional[str] = None):
    """
        Retrieve genome data for a specific patient and variant.

        - **patient_id**: The ID of the patient whose genome data is to be retrieved.
        - **rsid**: The ID of the variant to filter the genome data.

        Returns:
        - **JSONResponse**: Containing the genome data.
    """
    return genome_controller.get_patient_genome_data(patient_id, rsid)

@patient_genome_router.get("/patient_genome_data/expanded")
def get_patient_genome_data_expanded(patient_id: Optional[str] = None, rsid: Optional[str] = None):
    """
        Retrieve expanded genome data for a patient.

        - **patient_id**: An optional ID of the patient whose genome data is to be retrieved.
        - **rsid**: An optional ID of the variant to filter the genome data.
    """
    return genome_controller.get_patient_genome_data_expanded(patient_id, rsid)

@patient_genome_router.get("/full_report")
def get_full_report(patient_id: Optional[str] = None, rsid: Optional[str] = None):
    """
        Retrieve the full report for a specific patient and variant.

        - **patient_id**: Optional; The ID of the patient for whom the report is to be fetched.
        - **rsid**: Optional; The ID of the variant for which the report is to be fetched.

        Returns:
        - **JSONResponse**: Containing the full report data.
    """
    return genome_controller.get_full_report(patient_id, rsid)