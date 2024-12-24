from dotenv import load_dotenv
from typing import Any
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from routers import genome_router, notification_router 

load_dotenv()

root_router = APIRouter()

# root

@root_router.get("/")
def root():
    """
        Return a welcome message for the Genome Browser API.

        - **content**: A dictionary containing the welcome message.

        Returns:
        - **JSONResponse**: With a welcome message.
    """
    return JSONResponse(content={"Genome Browser API": "Welcome to Genome Browser API"})

# other routers

root_router.include_router(genome_router.genome_router, prefix="/genome", tags=["genome"])
root_router.include_router(notification_router.notification_router, prefix="/notification", tags=["notification"])