from sqlite3worker import Sqlite3Worker

class GenomeDatabase(object):
    __db_path = None
    sql_worker = ':memory:'

    def __init__(self):
        self.__db_path = "./data/genomes/genome.db" 
        self.sql_worker = Sqlite3Worker(self.__db_path) 

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

    # Write/Create/Update

    # SNP Pairs

    def update_or_insert_snp_pair(self, rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2):
        query = '''
            INSERT INTO snp_pairs (rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(rsid_genotypes) DO UPDATE SET magnitude=excluded.magnitude, risk=excluded.risk, notes=excluded.notes, rsid=excluded.rsid, allele1=excluded.allele1, allele2=excluded.allele2
        '''
        self.sql_worker.execute(query, (rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2))

    def save_snp_pairs_to_db(self, snp_df):
        for index, row in snp_df.iterrows():
            self.update_or_insert_snp_pair(row['rsid_genotypes'], row['magnitude'], row['risk'], row['notes'], row['rsid'], row['allele1'], row['allele2'])

    # Patient Genome Data

    def update_or_insert_patient(self, patient_id, patient_name):
        query = '''
            INSERT INTO patients (patient_id, patient_name)
            VALUES (?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET patient_name=excluded.patient_name
        '''
        self.sql_worker.execute(query, (patient_id, patient_name))

    def update_or_insert_patient_genome_data(self, rsid, patient_id, chromosome, position, genotype):
        query = '''
            INSERT INTO patient_genome_data (rsid, patient_id, chromosome, position, genotype)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(patient_id, rsid) DO UPDATE SET rsid=excluded.rsid, patient_id=excluded.patient_id, chromosome=excluded.chromosome, position=excluded.position, genotype=excluded.genotype
        '''
        self.sql_worker.execute(query, (rsid, patient_id, chromosome, position, genotype))

    def update_patient_and_genome_data(self, patient_df, patient_id, patient_name):
        self.update_or_insert_patient(patient_id, patient_name)
        for index, row in patient_df.iterrows():
            self.update_or_insert_patient_genome_data(row['rsid'], patient_id, row['chromosome'], row['position'], row['genotype'])

    # Read

    def fetch_snp_pairs_data(self):     
        query = '''
            SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
            FROM snp_pairs
        '''
        return self.sql_worker.execute(query)

    def fetch_joined_patient_data(self):
        query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
        '''
        return self.sql_worker.execute(query)