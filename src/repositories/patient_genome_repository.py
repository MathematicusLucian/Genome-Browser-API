from email.mime import base
import itertools
import json
import pandas as pd
from pydantic import ValidationError
from sqlite3worker import Sqlite3Worker
from utils import fetch_data_with_conditions
from models import Patient, PatientGenomeData

class PatientGenomeRepository:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.sql_worker = Sqlite3Worker(self.__db_path) 
        self.create_tables()

    def create_tables(self): 
        self.sql_worker.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                patient_name TEXT
            )
        ''')
        self.sql_worker.execute('''
            CREATE TABLE IF NOT EXISTS patient_genome_data (
                rsid TEXT NOT NULL,
                patient_id TEXT NOT NULL,
                chromosome TEXT NOT NULL,
                position INTEGER NOT NULL,
                genotype TEXT NOT NULL,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
                UNIQUE (patient_id, rsid)
            )
        ''')

    def close_connection(self):
        self.sql_worker.close()

    # WRITE (Create/Update/Insert)
 
    def update_or_insert_patient(self, patient: Patient):
        query = '''
            INSERT INTO patients (patient_id, patient_name)
            VALUES (?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET patient_name=excluded.patient_name
        '''
        self.sql_worker.execute(query, (patient.patient_id, patient.patient_name))

    def update_or_insert_patient_genome_data(self, patient_genome_data: PatientGenomeData):
        query = '''
            INSERT INTO patient_genome_data (rsid, patient_id, chromosome, position, genotype)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(patient_id, rsid) DO UPDATE SET rsid=excluded.rsid, patient_id=excluded.patient_id, chromosome=excluded.chromosome, position=excluded.position, genotype=excluded.genotype
        '''
        self.sql_worker.execute(query, (patient_genome_data.rsid, patient_genome_data.patient_id, patient_genome_data.chromosome, patient_genome_data.position, patient_genome_data.genotype))

    def update_patient_and_genome_data(self, patient_df, patient_id, patient_name):
        patient = Patient(patient_id=patient_id, patient_name=patient_name)
        self.update_or_insert_patient(patient)
        for index, row in patient_df.iterrows():
            patient_genome_data = PatientGenomeData(**row, patient_id=patient_id)
            self.update_or_insert_patient_genome_data(patient_genome_data)

    # READ (Fetch/Select)

    def fetch_patients(self, offset=0, **kwargs):
        columns_query = '''SELECT name FROM pragma_table_info('patients')'''
        columns = self.sql_worker.execute(columns_query)
        columns = list(itertools.chain.from_iterable(columns))
        base_query = '''
            SELECT *
            FROM patients
        ''' 
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)
    
    def fetch_patient_genome_data(self, offset=0, **kwargs): 
        columns_query = '''SELECT name FROM pragma_table_info('patient_genome_data')'''
        columns = self.sql_worker.execute(columns_query)
        columns = list(itertools.chain.from_iterable(columns))
        columns.remove("patient_id")
        base_query = '''
            SELECT rsid, chromosome, position, genotype
            FROM patient_genome_data
        '''
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)
        
    def fetch_snp_pairs_data_by_genotype(self, offset=0, **kwargs):     
        columns = ['rsid_genotypes', 'magnitude', 'risk', 'notes', 'rsid', 'allele1', 'allele2']
        base_query = '''
            SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
            FROM snp_pairs
        ''' 
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)
        
    def fetch_patient_data_expanded(self, offset=0, **kwargs): 
        columns = ['patient_id', 'patient_name', 'rsid', 'chromosome', 'position', 'genotype']
        base_query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
        '''
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)
    
    def fetch_full_report(self, offset=0, **kwargs):
        columns = ['patient_id', 'patient_name', 'rsid', 'chromosome', 'position', 'genotype',
               'rsid_genotypes', 'magnitude', 'risk', 'notes', 'allele1', 'allele2', 'genotype_match']
        base_query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype,
                   sp.rsid_genotypes, sp.magnitude, sp.risk, sp.notes, sp.allele1, sp.allele2,
                   (pgd.genotype = sp.allele1 || sp.allele2 OR pgd.genotype = sp.allele2 || sp.allele1) AS genotype_match
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
            JOIN snp_pairs sp ON pgd.rsid = sp.rsid
        '''
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)
