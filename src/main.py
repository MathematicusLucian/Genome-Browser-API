from fastapi import FastAPI
import uvicorn
from routers.root_router import root_router

# Routing
app = FastAPI(
    title="Genome Browser API",
    description="The Genome Browser API is a **FastAPI**-based (Python) server application (with **Uvicorn**), and which provides endpoints for managing and querying genome (gene variant) data (patient data is combined with SNP pairs data to show health risks.) SNP data is sourced from several sources, i.e. SNPedia, Ensembl, and GProfiler.",
    version="1.0.0"
)
app.include_router(root_router)

# Enable Swagger UI
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
app.redoc_url = "/redoc"

# MAIN
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)