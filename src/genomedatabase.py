import sqlite3
import uuid

class GenomeDatabase(object):
    def __init__(self, db_path=':memory:'):
        self.conn = sqlite3.connect(db_path)

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS snp_pairs (
                    rsid_genotypes TEXT,
                    magnitude REAL,
                    risk REAL,
                    notes TEXT,
                    rsid TEXT,
                    allele1 TEXT,
                    allele2 TEXT,
                    PRIMARY KEY (rsid_genotypes)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id TEXT PRIMARY KEY,
                    patient_name TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS patient_genome_data (
                    uuid TEXT PRIMARY KEY,
                    rsid TEXT,
                    patient_id TEXT,
                    chromosome TEXT,
                    position INTEGER,
                    genotype TEXT,
                    FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
                )
            ''')

    # Write/Create/Update

    def update_or_insert_snp_pairs(self, rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2):
        query = '''
            INSERT INTO snp_pairs (rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(rsid_genotypes) DO UPDATE SET magnitude=excluded.magnitude, risk=excluded.risk, notes=excluded.notes, rsid=excluded.rsid, allele1=excluded.allele1, allele2=excluded.allele2
        '''
        self.conn.execute(query, (rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2))
        self.conn.commit()

    def update_or_insert_patient(self, patient_id, patient_name):
        query = '''
            INSERT INTO patients (patient_id, patient_name)
            VALUES (?, ?)
            ON CONFLICT(patient_id) DO UPDATE SET patient_name=excluded.patient_name
        '''
        self.conn.execute(query, (patient_id, patient_name))
        self.conn.commit()

    def update_or_insert_patient_genome_data(self, rsid, patient_id, chromosome, position, genotype):
        query = '''
            INSERT INTO patient_genome_data (uuid, rsid, patient_id, chromosome, position, genotype)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(rsid) DO UPDATE SET chromosome=excluded.chromosome, position=excluded.position, genotype=excluded.genotype
        '''
        self.conn.execute(query, (uuid.uuid4(), rsid, patient_id, chromosome, position, genotype))
        self.conn.commit()

    def update_patient_and_genome_data(self, patient_id, patient_name, rsid, chromosome, position, genotype):
        self.update_or_insert_patient(patient_id, patient_name)
        self.update_or_insert_patient_genome_data(rsid, patient_id, chromosome, position, genotype)

    # Read

    def fetch_joined_patient_data(self):
        query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
        '''
        return self.conn.execute(query).fetchall()