import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from genomebrowser import GenomeBrowser

load_dotenv()
snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')

def setup():
    return GenomeBrowser(snp_pairs_file_name_with_path)

app = FastAPI()
# Enable Swagger UI
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"

# root

@app.get("/")
def root():
    return {"Genome Browser API": "Welcome to Genome Browser API"}

# /genome

@app.post("/genome/load_patient/{genome_file_name_with_path}")
def load_genome(genome_file_name_with_path: str):
    genome_browser.load_genome(genome_file_name_with_path) 
    return {"Genome Loaded": genome_file_name_with_path}

@app.get("/genome/full_report")
def get_full_report():
    full_report = genome_browser.fetch_full_report()
    return {"Full Report": full_report}

# /genome_variant

@app.get("/gene_variant/full_report/{variant_id}")
def get_gene_variant(variant_id: str):
    gene_variant = genome_browser.fetch_full_report_by_gene_variant(variant_id)
    return {"Gene Variant": gene_variant}

@app.get("/gene_variant/patient_details/{variant_id}")
def get_patient_details(variant_id: str):
    details = genome_browser.fetch_gene_variant_patient_details(variant_id)
    return {"Patient Details": details}

@app.get("/gene_variant/research/{variant_id}")
def get_research(variant_id: str):
    research = genome_browser.fetch_gene_variant_research(variant_id)
    return {"Research": research}

if __name__ == "__main__":
    app.redoc_url = "/redoc"
    genome_browser = setup()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)