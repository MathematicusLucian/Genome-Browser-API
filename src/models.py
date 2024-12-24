from pydantic import BaseModel

class SnpPair(BaseModel):
    rsid_genotypes: str
    magnitude: float
    risk: float
    notes: str
    rsid: str
    allele1: str
    allele2: str

class Patient(BaseModel):
    patient_id: str
    patient_name: str

class PatientGenomeData(BaseModel):
    rsid: str
    patient_id: str
    chromosome: str
    position: int
    genotype: str
