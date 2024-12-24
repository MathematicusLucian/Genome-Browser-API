import os
from dotenv import load_dotenv
from typing import Any, Callable, Optional
from fastapi import APIRouter, Depends, WebSocketDisconnect
from fastapi.params import Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.openapi.utils import get_openapi
import threading 
from controllers.genome_controller import GenomeController
from controllers.websocket_controller import WebSocketController
from services.genome_service import GenomeService
from services.websocket_service import WebSocketService

load_dotenv()

router = APIRouter()
genome_service = GenomeService()
websocket_service = WebSocketService()

def custom_openapi():
    if router.openapi_schema:
        return router.openapi_schema
    openapi_schema = get_openapi(
        title="WebSocket API",
        version="1.0.0",
        description="This is a simple WebSocket API",
        routes=router.routes,
    )
    openapi_schema["paths"]["/ws"] = {
        "get": {
            "summary": "WebSocket connection",
            "description": "Connect to the WebSocket server. Send a message and receive a response.",
            "responses": {
                "101": {
                    "description": "Switching Protocols - The client is switching protocols as requested by the server.",
                }
            }
        }
    }
    router.openapi_schema = openapi_schema
    return router.openapi_schema

router.openapi = custom_openapi

# root

@router.get("/")
def root():
    """
        Return a welcome message for the Genome Browser API.

        - **content**: A dictionary containing the welcome message.

        Returns:
        - **JSONResponse**: With a welcome message.
    """
    return JSONResponse(content={"Genome Browser API": "Welcome to Genome Browser API"})

# Patient Genome: /patient

@router.post("/load_genome")
def load_genome(genome_file_name_with_path: Optional[str] = Query(None)): 
    """
        Load a genome file in the background.
        
        - **genome_file_name_with_path**: Optional; The path to the genome file to be loaded.

        Returns:
        - **JSONResponse**: Indicating that genome loading has commenced and the path to the genome file.
    """
    threading.Thread(target=genome_service.load_genome_background, args=(genome_file_name_with_path,)).start()
    return JSONResponse(content={"message": "Genome loading commenced", "genome_file_name_with_path": genome_file_name_with_path})

# Notify UI or log the completion of data loading activity
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    """
        WebSocket endpoint for real-time communication.

        - **Websocket**: The WebSocket connection instance.
    """
    await websocket_service.websocket_endpoint(websocket)

# List of All Patients

@router.get("/patients")
def get_full_report():
    """
        Retrieve the full report of patients.

        - **full_report**: A JSON object containing the full report of patients.

        Returns:
        - **JSONResponse**: A response object containing the full report in JSON format.
    """
    full_report = genome_service.fetch_patients()
    return JSONResponse(content=full_report)

# General Human Genome

@router.get("/snp_research")
def get_snp_research(variant_id: Optional[str] = None):
    """
        Retrieve SNP research data.

        - **variant_id**: An optional string representing the variant ID.

        Returns:
        - **JSONResponse**: Containing SNP research data.
    """
    return JSONResponse(content=genome_service.fetch_all_snp_pairs(variant_id=variant_id))

# Chromosomes
@router.get("/fetch_chromosomes/ensembl")
def get_list_of_chromosomes_from_ensembl_api(): 
    """
        Fetch the list of chromosomes from the Ensembl API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return JSONResponse(content=genome_service.fetch_chromosomes_from_ensembl())

@router.get("/fetch_chromosomes/gprofiler")
def get_list_of_chromosomes_from_gprofiler_api(): 
    """
        Fetch the list of chromosomes from the g:Profiler API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return JSONResponse(content=genome_service.fetch_chromosomes_from_gprofiler())

@router.get("/fetch_gene_by_variant")
def get_from_gprofiler_api_gene_data_matching_variant_rsid(variant_id: Optional[str] = None):
    """
        Fetch gene data matching a variant RSID from the g:Profiler API.

        - **variant_id**: Optional; The RSID of the variant to fetch gene data for. (The fallback is 'rs11734132'.")

        Returns:
        - **JSONResponse**: Containing the details of the gene matching the variant RSID.
    """
    return JSONResponse(content=genome_service.fetch_gene_data_by_variant(variant_id))

# Fetch Patient Data

@router.get("/patient_profile")
def get_patient_genome_data(patient_id: Optional[str] = None):
    """
        Retrieve genome data for a specific patient.

        - **patient_id**: An optional string representing the ID of the patient whose genome data is to be fetched.

        Returns:
        - **JSONResponse**: Containing the patient's genome data.
    """
    return JSONResponse(content=genome_service.fetch_patient_profile(patient_id))

@router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve genome data for a specific patient and variant.

        - **patient_id**: The ID of the patient whose genome data is to be retrieved.
        - **variant_id**: The ID of the variant to filter the genome data.

        Returns:
        - **JSONResponse**: Containing the genome data.
    """
    return JSONResponse(content=genome_service.fetch_patient_genome_data(patient_id, variant_id))

@router.get("/patient_genome_data/expanded")
def get_patient_genome_data_expanded(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve expanded genome data for a patient.

        - **patient_id**: An optional ID of the patient whose genome data is to be retrieved.
        - **variant_id**: An optional ID of the variant to filter the genome data.
    """
    return JSONResponse(content=genome_service.fetch_patient_data_expanded(patient_id, variant_id))

@router.get("/full_report")
def get_full_report(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    """
        Retrieve the full report for a specific patient and variant.

        - **patient_id**: Optional; The ID of the patient for whom the report is to be fetched.
        - **variant_id**: Optional; The ID of the variant for which the report is to be fetched.

        Returns:
        - **JSONResponse**: Containing the full report data.
    """
    return JSONResponse(content=genome_service.fetch_full_report(patient_id, variant_id))
