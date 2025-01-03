from dotenv import load_dotenv
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.params import Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel  
from controllers.genome_controller import GenomeController

load_dotenv()

snp_research_router = APIRouter() 
genome_controller = GenomeController()

class RsidsPayload(BaseModel):
    rsidsList: List[str]  # Define the expected structure of the payload

def is_list_of_strings(variable) -> bool:
    if not isinstance(variable, list):
        return False
    return all(isinstance(item, str) for item in variable)

# Data from published genome research, e.g. SNP Pairs for gene variants
@snp_research_router.post("/")
async def get_snp_research(payload: RsidsPayload):
    """
    Retrieve SNP research data.

    - **rsidsList**: A list of strings representing variant IDs.

    Returns:
    - **JSONResponse**: Containing SNP research data.
    """
    rsid = payload.rsidsList  # Extract the rsidsList field
    print('Received rsid:', rsid)

    # Validate the list length
    if len(rsid) < 1 or len(rsid) > 10:
        raise HTTPException(
            status_code=400,
            detail="The rsidsList must contain between 1 and 10 items."
        )
    
    # Call the genome controller to get the SNP research data
    return genome_controller.get_snp_research(rsid)

# E.g Body:
# ["rs1000113", "rs1000597" ]
@snp_research_router.get("/by-genotype")
def get_snp_pairs_data_by_genotype(rsid: Optional[str] = None, allele1: Optional[str] = None, allele2: Optional[str] = None):
    """
        Retrieve SNP research data.

        - **rsid**: An optional string representing the variant ID.
        - **allele1**: An optional string representing allele1.
        - **allele2**: An optional string representing allele2.

        Returns:
        - **JSONResponse**: Containing SNP research data.
    """
    return genome_controller.get_snp_pairs_data_by_genotype(rsid) 

# Chromosomes
@snp_research_router.get("/fetch_chromosomes/ensembl")
def get_list_of_chromosomes_from_ensembl_api(): 
    """
        Fetch the list of chromosomes from the Ensembl API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return genome_controller.get_list_of_chromosomes_from_ensembl_api()

@snp_research_router.get("/fetch_chromosomes/gprofiler")
def get_list_of_chromosomes_from_gprofiler_api(): 
    """
        Fetch the list of chromosomes from the g:Profiler API.

        Returns:
        - **JSONResponse**: Containing the list of chromosomes.
    """
    return genome_controller.get_list_of_chromosomes_from_gprofiler_api()

@snp_research_router.get("/fetch_gene_by_variant")
def get_from_gprofiler_api_gene_data_matching_variant_rsid(rsid: Optional[str] = None):
    """
        Fetch gene data matching a variant RSID from the g:Profiler API.

        - **rsid**: Optional; The RSID of the variant to fetch gene data for. (The fallback is 'rs11734132'.")

        Returns:
        - **JSONResponse**: Containing the details of the gene matching the variant RSID.
    """
    return genome_controller.get_from_gprofiler_api_gene_data_matching_variant_rsid(rsid) 