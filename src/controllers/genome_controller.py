from typing import Optional
from fastapi import Query
from fastapi.responses import JSONResponse
import threading
from services.genome_service import GenomeService

class GenomeController:
    def __init__(self):
        self.genome_service = GenomeService()

    def load_genome(self, genome_file_name_with_path: Optional[str] = Query(None)): 
        threading.Thread(target=self.genome_router.load_genome_background, args=(genome_file_name_with_path,)).start()
        return JSONResponse(content={"message": "Genome loading commenced", "genome_file_name_with_path": genome_file_name_with_path})

    def get_snp_research(self, rsid: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_all_snp_pairs(rsid=rsid))
    
    def get_snp_pairs_data_by_genotype(self, rsid: Optional[str] = None, allele1: Optional[str] = None, allele2: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_snp_pairs_data_by_genotype(rsid=rsid, allele1=allele1, allele2=allele2))

    def get_list_of_chromosomes_from_ensembl_api(self): 
        return JSONResponse(content=self.genome_service.fetch_chromosomes_from_ensembl())

    def get_list_of_chromosomes_from_gprofiler_api(self): 
        return JSONResponse(content=self.genome_service.fetch_chromosomes_from_gprofiler())

    def get_from_gprofiler_api_gene_data_matching_variant_rsid(self, rsid: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_gene_data_by_variant(rsid=rsid))

    def get_patient_profile(self, patient_id: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_patient_profile(patient_id=patient_id)) 

    def get_patient_genome_data(self, patient_id: Optional[str] = None, rsid: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_patient_genome_data(patient_id=patient_id, rsid=rsid))

    def get_patient_genome_data_expanded(self, patient_id: Optional[str] = None, rsid: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_patient_data_expanded(patient_id=patient_id, rsid=rsid))

    def get_full_report(self, patient_id: Optional[str] = None, rsid: Optional[str] = None):
        return JSONResponse(content=self.genome_service.fetch_full_report(patient_id=patient_id, rsid=rsid))
