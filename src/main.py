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

# Patient Genome: /patient

@app.post("/load_genome/{genome_file_name_with_path}")
def load_genome(genome_file_name_with_path: str):
    if(genome_file_name_with_path == "default"):
        genome_file_name_with_path = default_genome_file_name_with_path
    genome_browser.load_genome(genome_file_name_with_path) 
    return {"Genome Loaded": genome_file_name_with_path,
            "Number of Rows": genome_browser.patient_genome_df.size}

# List of All Patients
@app.get("/patients")
def get_full_report():
    full_report = genome_browser.fetch_patients()
    return {"Patient": full_report}

# Patient SNP Pairs Matches

@app.get("/snp_research")
def get_snp_research():
    full_report = genome_browser.fetch_all_snp_pairs() 
    return {"SNP Pairs": full_report}

@app.get("/snp_research/{patient_id}")
def get_snp_research_patient_id(patient_id: str):
    full_report = genome_browser.fetch_all_snp_pairs(patient_id) 
    return {"SNP Pairs": full_report}

@app.get("/snp_research/{patient_id}/{variant_id}")
def get_snp_research_patient_id_rsid(patient_id: str, variant_id: str):
    full_report = genome_browser.fetch_all_snp_pairs(patient_id, variant_id) 
    return {"SNP Pairs": full_report}

# Individual Patient Data

@app.get("/patient_genome_data")
def get_patient_genome_data():
    full_report = genome_browser.fetch_patient_data_genotypes() 
    return {"SNP Pairs": full_report}

@app.get("/patient_genome_data/{patient_id}")
def get_patient_genome_data_patient_id(patient_id: str):
    full_report = genome_browser.fetch_patient_data_genotypes(patient_id) 
    return {"SNP Pairs": full_report}

@app.get("/patient_genome_data/{patient_id}/{variant_id}")
def get_patient_genome_data_patient_id_rsid(patient_id: str, variant_id: str):
    full_report = genome_browser.fetch_patient_data_genotypes(patient_id, variant_id) 
    return {"SNP Pairs": full_report}
        
# Individual Patient Data Expanded (Featuring Their Genotypes)

@app.get("/patient_genome_data/expanded")
def get_patient_genome_data():
    expanded_patient_data = genome_browser.fetch_patient_data_expanded() 
    return {"Expanded": expanded_patient_data}

@app.get("/patient_genome_data/expanded/{patient_id}")
def get_patient_genome_data_patient_id(patient_id: str):
    expanded_patient_data = genome_browser.fetch_patient_data_expanded(patient_id) 
    return {"SNP Pairs": expanded_patient_data}

@app.get("/patient_genome_data/expanded/{patient_id}/{variant_id}")
def get_patient_genome_data_patient_id_rsid(patient_id: str, variant_id: str):
    expanded_patient_data = genome_browser.fetch_patient_data_expanded(patient_id, variant_id) 
    return {"SNP Pairs": expanded_patient_data} 

# Patient Data plus SNP Matches

@app.get("/full_report")
def get_full_report():
    full_report = genome_browser.fetch_full_report()
    return {"Full Report": full_report}

@app.get("/full_report/{patient_id}")
def get_full_report_patient_id(patient_id: str):
    full_report = genome_browser.fetch_full_report(patient_id)
    return {"Full Report": full_report}

@app.get("/full_report/{patient_id}/{variant_id}")
def get_full_report_patient_id_rsid(patient_id: str, variant_id: str):
    full_report = genome_browser.fetch_full_report(patient_id, variant_id) 
    return {"Full Report": full_report}

# MAIN

if __name__ == "__main__":
    app.redoc_url = "/redoc"
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)