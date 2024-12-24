import os
from dotenv import load_dotenv
from typing import Any, Callable, Optional
from fastapi import APIRouter, Depends, WebSocketDisconnect
from fastapi.params import Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.openapi.utils import get_openapi
import threading
import asyncio
from genomebrowser import GenomeBrowser
from genomedatabase import GenomeDatabase

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

load_dotenv()
snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
default_genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')

websocket_url = "ws://localhost:8000/ws"

async def notify_ui(genome_file_name_with_path: str):
    async with WebSocket(websocket_url, headers=None, subprotocols=None) as websocket:
        await websocket.send_json({"event": "genome_loaded", "genome_file_name_with_path": genome_file_name_with_path, "Number of Rows": genome_browser.patient_genome_df.size})

def load_genome_background(genome_file_name_with_path: Optional[str] = None):
    if genome_file_name_with_path is None: genome_file_name_with_path = "default"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = loop.run_in_executor(None, genome_browser.load_genome, genome_file_name_with_path)
    loop.run_until_complete(future)
    # Notify UI or log the completion
    loop.run_until_complete(notify_ui(genome_file_name_with_path))
    loop.close()
    
router = APIRouter()
router.openapi = custom_openapi

genome_browser = GenomeBrowser(
    snp_pairs_file_name_with_path=snp_pairs_file_name_with_path,
    default_genome_file_name_with_path=default_genome_file_name_with_path,
    genome_database=GenomeDatabase()
) 

# root

@router.get("/")
def root():
    return JSONResponse(content={"Genome Browser API": "Welcome to Genome Browser API"})

# Patient Genome: /patient

@router.post("/load_genome")
def load_genome(genome_file_name_with_path: Optional[str] = Query(None)): 
    threading.Thread(target=load_genome_background, args=(genome_file_name_with_path,)).start()
    return JSONResponse(content={"message": "Genome loading commenced", "genome_file_name_with_path": genome_file_name_with_path})

# Notify UI or log the completion of data loading activity
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket): 
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"WebSocket connection closed: {e}")

# List of All Patients

@router.get("/patients")
def get_full_report():
    full_report = genome_browser.fetch_patients()
    return JSONResponse(content=full_report)

# Fetch Patient Data

def fetch_data(fetch_method: Callable, **kwargs) -> Any:
    filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None and v != ""}
    return fetch_method(**filtered_kwargs)

@router.get("/snp_research")
def get_snp_research(variant_id: Optional[str] = None):
    return JSONResponse(content=fetch_data(genome_browser.fetch_all_snp_pairs, variant_id=variant_id))

@router.get("/patient_profile")
def get_patient_genome_data(patient_id: Optional[str] = None):
    return JSONResponse(content=fetch_data(fetch_method=genome_browser.fetch_patient_profile, patient_id=patient_id))

@router.get("/patient_genome_data")
def get_patient_genome_data(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return JSONResponse(content=fetch_data(fetch_method=genome_browser.fetch_patient_genome_data, patient_id=patient_id, variant_id=variant_id))

@router.get("/patient_genome_data/expanded")
def get_patient_genome_data_expanded(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return JSONResponse(content=fetch_data(genome_browser.fetch_patient_data_expanded, patient_id=patient_id, variant_id=variant_id))

@router.get("/full_report")
def get_full_report(patient_id: Optional[str] = None, variant_id: Optional[str] = None):
    return JSONResponse(content=fetch_data(genome_browser.fetch_full_report, patient_id=patient_id, variant_id=variant_id))
