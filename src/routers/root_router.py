from dotenv import load_dotenv
from typing import Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from routers import notification_router, patient_genome_router, snp_research_router

load_dotenv()

root_router = APIRouter()

# root

@root_router.get("/")
def root():
    """
        Return a welcome message for the GenomeSearch API.

        - **content**: A dictionary containing the welcome message.

        Returns:
        - **JSONResponse**: With a welcome message.
    """
    return JSONResponse(content={"GenomeSearch API": "Welcome to GenomeSearch API"})

# other routers

root_router.include_router(snp_research_router.snp_research_router, prefix="/snp_research", tags=["snp_research"])
root_router.include_router(patient_genome_router.patient_genome_router, prefix="/patient_genome", tags=["patient_genome"])
root_router.include_router(notification_router.notification_router, prefix="/notification", tags=["notification"])