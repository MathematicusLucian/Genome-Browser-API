from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.root_router import root_router

# Routing
app = FastAPI(
    title="GenomeSearch API",
    description="The GenomeSearch API is a **FastAPI**-based (Python) server application (with **Uvicorn**), and which provides endpoints for managing and querying genome (gene variant) data (patient data is combined with SNP pairs data to show health risks.) SNP data is sourced from several sources, i.e. SNPedia, Ensembl, and GProfiler.",
    version="1.0.0"
)
app.include_router(root_router)

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",  
    "http://192.168.1.149:3000", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Swagger UI
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
app.redoc_url = "/redoc"

# MAIN
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)