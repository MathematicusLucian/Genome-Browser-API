import asyncio
import sys
from typing import Optional
from fastapi.websockets import WebSocket
from gprofiler import GProfiler
import requests
from genome_browser import GenomeBrowser
from genome_db_manager import GenomeDatabase
import os

class GenomeService:
    def __init__(self):
        self.genome_browser = GenomeBrowser(
            snp_pairs_file_name_with_path=os.getenv('SNP_PAIRS_FILE_PATH'),
            default_genome_file_name_with_path=os.getenv('GENOME_FILE_PATH'),
            genome_repository=GenomeDatabase(db_path=os.getenv('SQLITE_DATABASE_PATH'))
        )

    async def notify_ui(self, genome_file_name_with_path: str):
        websocket_url = "ws://localhost:8000/ws"
        async with WebSocket(websocket_url, headers=None, subprotocols=None) as websocket:
            await websocket.send_json({"event": "genome_loaded", "genome_file_name_with_path": genome_file_name_with_path, "Number of Rows": self.genome_browser.patient_genome_df.size})

    def load_genome_background(self, genome_file_name_with_path: Optional[str] = None):
        if genome_file_name_with_path is None: genome_file_name_with_path = "default"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = loop.run_in_executor(None, self.genome_browser.load_genome, genome_file_name_with_path)
        loop.run_until_complete(future)
        loop.run_until_complete(self.notify_ui(genome_file_name_with_path))
        loop.close()

    def fetch_patients(self):
        return self.genome_browser.fetch_patients()

    def fetch_all_snp_pairs(self, variant_id: Optional[str] = None):
        return self.genome_browser.fetch_all_snp_pairs(variant_id=variant_id)

    def fetch_chromosomes_from_ensembl(self):
        server = "https://grch37.rest.ensembl.org"
        ext = "/info/assembly/homo_sapiens?"
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        return repr(decoded)

    def fetch_chromosomes_from_gprofiler(self):
        organism = 'hsapiens'
        gp = GProfiler(return_dataframe=True)
        data = gp.convert(organism=organism, query='*')
        return data

    def fetch_gene_data_by_variant(self, variant_id: Optional[str] = None):
        if variant_id == None: variant_id = "rs11734132"
        gp = GProfiler(return_dataframe=True)
        data = gp.snpense(query=[variant_id])
        return data['gene_names']

    def fetch_patient_profile(self, patient_id: Optional[str] = None):
        return self.genome_browser.fetch_patient_profile(patient_id=patient_id)

    def fetch_patient_genome_data(self, patient_id: Optional[str] = None, variant_id: Optional[str] = None):
        return self.genome_browser.fetch_patient_genome_data(patient_id=patient_id, variant_id=variant_id)

    def fetch_patient_data_expanded(self, patient_id: Optional[str] = None, variant_id: Optional[str] = None):
        return self.genome_browser.fetch_patient_data_expanded(patient_id=patient_id, variant_id=variant_id)

    def fetch_full_report(self, patient_id: Optional[str] = None, variant_id: Optional[str] = None):
        return self.genome_browser.fetch_full_report(patient_id=patient_id, variant_id=variant_id)
