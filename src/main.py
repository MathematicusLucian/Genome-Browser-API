import os
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn
from genomebrowser import GenomeBrowser
from genomedatabase import GenomeDatabase
from utils import check_if_default

load_dotenv()
snp_pairs_file_name_with_path = os.getenv('SNP_PAIRS_FILE_PATH')
default_genome_file_name_with_path = os.getenv('GENOME_FILE_PATH')

def setup_genome_browser():
    return GenomeBrowser(snp_pairs_file_name_with_path=snp_pairs_file_name_with_path, genome_database=GenomeDatabase())

app = FastAPI()
# Enable Swagger UI
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
genome_browser = setup_genome_browser()

# root

@app.get("/")
def root():
    return {"Genome Browser API": "Welcome to Genome Browser API"}

# /genome

@app.post("/genome/load_patient/{genome_file_name_with_path}")
def load_genome(genome_file_name_with_path: str):
    if(genome_file_name_with_path == "default"):
        genome_file_name_with_path = default_genome_file_name_with_path
    genome_browser.load_genome(genome_file_name_with_path) 
    return {"Genome Loaded": genome_file_name_with_path,
            "Number of Rows": genome_browser.patient_genome_df.size}

@app.get("/genome/full_report")
def get_full_report():
    full_report = genome_browser.fetch_full_report()
    return {"Full Report": full_report}

# /genome_variant

@app.get("/gene_variant/full_report/{variant_id}")
def get_gene_variant(variant_id: str):
    variant_id = check_if_default(variant_id)
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

# MAIN

if __name__ == "__main__":
    app.redoc_url = "/redoc"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)