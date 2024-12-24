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

    # WRITE (Create/Update/Insert)

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

    # READ (Fetch/Select)

    # Patient SNP Pairs Matches
    
    # SNP Pairs data 
    
    def fetch_snp_pairs_data(self, offset=0, **kwargs): 
        base_query = '''
            SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
            FROM snp_pairs
        '''
        conditions = []
        params = []
        if 'patient_id' in kwargs:
            conditions.append('patient_id = ?')
            params.append(kwargs['patient_id'])
        if 'variant_id' in kwargs:
            conditions.append('rsid = ?')
            params.append(kwargs['variant_id'])
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
        base_query += ' LIMIT 25 OFFSET ?'
        params.append(offset)
        return self.sql_worker.execute(base_query, tuple(params))

    # List of All Patients

    def fetch_patients_list(self, offset=0):
        query = '''
            SELECT *
            FROM patients
            LIMIT 25 OFFSET ?
        '''
        return self.sql_worker.execute(query, (offset,))

    # Individual Patient Profiles

    def fetch_patient_profile(self, offset=0, **kwargs):
        base_query = '''
            SELECT *
            FROM patients
        '''
        conditions = []
        params = []
        if 'patient_id' in kwargs:
            conditions.append('patient_id = ?')
            params.append(kwargs['patient_id'])
        if 'variant_id' in kwargs:
            conditions.append('rsid = ?')
            params.append(kwargs['variant_id'])
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
        base_query += ' LIMIT 25 OFFSET ?'
        params.append(offset)
        return self.sql_worker.execute(base_query, tuple(params))
    
    # Individual Patient Genotype Datasets
    
    def fetch_patient_data_genotypes(self, offset=0, **kwargs):
        # base_query = '''SELECT DISTINCT m.name || '.' || ii.name AS 'indexed-columns'
        #     FROM sqlite_schema AS m,
        #         pragma_index_list(m.name) AS il,
        #         pragma_index_info(il.name) AS ii
        #     WHERE m.type='table'
        #     ORDER BY 1
        # '''
        base_query = '''
            SELECT * 
            FROM patient_genome_data
        '''
        # SELECT * FROM pragma_index_info('patient_genome_data')
        # PRAGMA index_info('patient_genome_data')

        # conditions = []
        # params = []
        # if 'patient_id' in kwargs:
        #     conditions.append('patient_id = ?')
        #     params.append(kwargs['patient_id'])
        # if 'variant_id' in kwargs:
        #     conditions.append('rsid = ?')
        #     params.append(kwargs['variant_id'])
        # if conditions:
        #     base_query += ' WHERE ' + ' AND '.join(conditions)
        # base_query += ' LIMIT 25 OFFSET ?'
        # params.append(offset)
        
        # Execute the query and fetch the results
        # result = self.sql_worker.execute(base_query, tuple(params))
        result = self.sql_worker.execute(base_query)
        return result
    
    # def fetch_patient_genome_data_columns(self):
    #     query = 'PRAGMA table_info(patient_genome_data)'
    #     columns_info = self.sql_worker.execute(query)
    #     columns = [col[1] for col in columns_info]
    #     return columns
        
        # # Retrieve column names from the table schema
        # column_query = 'PRAGMA table_info(patient_genome_data)'
        # columns_info = self.sql_worker.execute(column_query)
        # columns = [col[1] for col in columns_info]
        
        # # Combine column names with the result data
        # data = [dict(zip(columns, row)) for row in result]
        # return data
        
    # Individual Patient Data by Genotype

    def fetch_snp_pairs_data_by_genotype(self, patient_id, rsid, allele1, allele2, offset=0):     
        query = '''
            SELECT rsid_genotypes, magnitude, risk, notes, rsid, allele1, allele2
            FROM snp_pairs
            WHERE patient_id = ? AND rsid = ? AND allele1 = ? AND allele2 = ?
            LIMIT 25 OFFSET ?
        '''
        return self.sql_worker.execute(query, (patient_id, rsid, allele1, allele2, offset,))
        
    # Individual Patient Data Expanded (Featuring Their Genotypes)
    
    def fetch_joined_patient_data(self, offset=0, **kwargs):
        base_query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype,
                   sp.rsid_genotypes, sp.magnitude, sp.risk, sp.notes, sp.allele1, sp.allele2,
                   (pgd.genotype = sp.allele1 || sp.allele2 OR pgd.genotype = sp.allele2 || sp.allele1) AS genotype_match
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
            JOIN snp_pairs sp ON pgd.rsid = sp.rsid
        '''
        conditions = []
        params = []
        if 'patient_id' in kwargs:
            conditions.append('pgd.patient_id = ?')
            params.append(kwargs['patient_id'])
        if 'variant_id' in kwargs:
            conditions.append('pgd.rsid = ?')
            params.append(kwargs['variant_id'])
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
        base_query += ' LIMIT 25 OFFSET ?'
        params.append(offset)
        result = self.sql_worker.execute(base_query, tuple(params))
        columns = [desc[0] for desc in self.sql_worker.cursor.description]
        data = [dict(zip(columns, row)) for row in result]
        return data
    
    # Patient Data plus SNP Matches
 
    def fetch_joined_patient_data(self, offset=0, **kwargs):
        base_query = '''
            SELECT p.patient_id, p.patient_name, pgd.rsid, pgd.chromosome, pgd.position, pgd.genotype,
                   sp.rsid_genotypes, sp.magnitude, sp.risk, sp.notes, sp.allele1, sp.allele2,
                   (pgd.genotype = sp.allele1 || sp.allele2 OR pgd.genotype = sp.allele2 || sp.allele1) AS genotype_match
            FROM patients p
            JOIN patient_genome_data pgd ON p.patient_id = pgd.patient_id
            JOIN snp_pairs sp ON pgd.rsid = sp.rsid
        '''
        conditions = []
        params = []
        if 'patient_id' in kwargs:
            conditions.append('pgd.patient_id = ?')
            params.append(kwargs['patient_id'])
        if 'variant_id' in kwargs:
            conditions.append('pgd.rsid = ?')
            params.append(kwargs['variant_id'])
        if conditions:
            base_query += ' WHERE ' + ' AND '.join(conditions)
        base_query += ' LIMIT 25 OFFSET ?'
        params.append(offset)
        return self.sql_worker.execute(base_query, tuple(params))