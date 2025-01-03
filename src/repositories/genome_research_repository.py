from email.mime import base
import itertools
import json
import pandas as pd
from pydantic import ValidationError
from sqlite3worker import Sqlite3Worker
from utils import fetch_data_with_conditions
from models import SnpPair 

class GenomeResearchRepository:
    def __init__(self, db_path):
        self.__db_path = db_path
        self.sql_worker = Sqlite3Worker(self.__db_path) 
        self.create_tables()

    def create_tables(self):
        self.sql_worker.execute('''
            CREATE TABLE IF NOT EXISTS snp_pairs (
                rsid_genotypes TEXT NOT NULL,
                magnitude REAL,
                risk REAL,
                notes TEXT,
                rsid TEXT NOT NULL,
                allele1 TEXT NOT NULL,
                allele2 TEXT NOT NULL,
                PRIMARY KEY (rsid_genotypes)
                UNIQUE (rsid_genotypes)
            )
        ''') 

    def close_connection(self):
        self.sql_worker.close()

    # WRITE (Create/Update/Insert)

    def update_or_insert_snp_pair(self, snp_pair: SnpPair):
        query = '''
            INSERT INTO snp_pairs (rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(rsid_genotypes) DO UPDATE SET magnitude=excluded.magnitude, risk=excluded.risk, notes=excluded.notes, rsid=excluded.rsid, allele1=excluded.allele1, allele2=excluded.allele2
        '''
        self.sql_worker.execute(query, (snp_pair.rsid_genotypes, snp_pair.magnitude, snp_pair.risk, snp_pair.notes, snp_pair.rsid, snp_pair.allele1, snp_pair.allele2))

    def save_snp_pairs_to_db(self, snp_df):
        for index, row in snp_df.iterrows():
            try:
                # Ensure 'notes' is a string
                row['notes'] = str(row['notes']) if pd.notna(row['notes']) else ''
                snp_pair = SnpPair(**row)
                # Save snp_pair to the database
                self.update_or_insert_snp_pair(snp_pair) 
            except ValidationError as e:
                print(f"Validation error: {e}") 

    # READ (Fetch/Select) 

    def fetch_snp_pairs_data(self, offset=0, **kwargs): 
        columns_query = '''SELECT name FROM pragma_table_info('snp_pairs')'''
        columns = self.sql_worker.execute(columns_query)
        print('columns', columns)   
        columns = list(itertools.chain.from_iterable(columns))
        # base_query = '''
        #     SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
        #     FROM snp_pairs 
        # '''  
        # Construct the query dynamically with parameter substitution
        rsids = kwargs.get('rsid') # kwargs['rsid']
        print('rsids', rsids)   
        # rsids = ['rs1064793444', 'rs1064793273', 'rs1064793267']
        placeholders = ', '.join('?' for _ in rsids)
        results_list = self.sql_worker.execute(f"""
            SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
            FROM snp_pairs
            WHERE rsid IN {tuple(rsids)}
        """)
        print('results_list', results_list)
        results_list = pd.DataFrame(results_list, columns=columns)
        json_str = results_list.to_json(orient='records', date_format='iso')
        return json.loads(json_str) 
    
    def fetch_genes_in_genome(self, offset=0, **kwargs): 
        columns_query = '''SELECT name FROM pragma_table_info('snp_pairs')'''
        columns = self.sql_worker.execute(columns_query)
        columns = list(itertools.chain.from_iterable(columns))
        base_query = '''
            SELECT genes 
            FROM snp_pairs
        ''' 
        sql_worker_execution_function = self.sql_worker.execute
        return fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs)