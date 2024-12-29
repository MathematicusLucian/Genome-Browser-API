import json
from venv import logger
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def load_file(file_name_with_path, names=None, straight: bool = False):
    params_list = {'sep': '\t', 'comment': '#', 'names': names}
    params = None
    params = {k: v for k, v in params_list.items() if straight is False} 
    return pd.read_csv(file_name_with_path, low_memory=False, **params) 

def check_if_default(rsid):
    if rsid == "default":
        rsid = "rs10516809"
    return rsid

def fetch_data_with_conditions(base_query, columns, offset, sql_worker_execution_function, **kwargs):
    conditions = []
    params = []
    # Determine if the query has a join by checking for the presence of 'JOIN' keyword
    has_join = 'JOIN' in base_query.upper()        
    # Adjust the column prefix based on whether a join is present
    patient_id_column = 'pgd.patient_id' if has_join else 'patient_id'
    rsid_column = 'pgd.rsid' if has_join else 'rsid'
    allele1_column = 'pgd.allele1' if has_join else 'allele1'
    allele2_column = 'pgd.allele2' if has_join else 'allele2'
    if 'patient_id' in kwargs and kwargs['patient_id'] is not None:
        conditions.append(f'{patient_id_column} = ?')
        params.append(kwargs['patient_id'])
    if 'allele1' in kwargs and kwargs['allele1'] is not None:
        conditions.append(f'{allele1_column} = ?')
        params.append(kwargs['allele1'])
    if 'allele2' in kwargs and kwargs['allele2'] is not None:
        conditions.append(f'{allele2_column} = ?')
        params.append(kwargs['allele2']) 
    if 'rsid' in kwargs and kwargs['rsid'] is not None:
        print(kwargs['rsid'])
        if(type(kwargs['rsid'] == list)):
            print('list')
            rsids = "('"+"','".join(kwargs['rsid'])+"')"
            base_query += f' WHERE rsid IN {rsids} ' 
            base_query += f' LIMIT 25 OFFSET {offset}' 
        else:
            conditions.append(f'{rsid_column} = ?')
        params.append(kwargs['rsid'])
    if conditions:
        base_query += ' WHERE ' + ' AND '.join(conditions)
        base_query += ' LIMIT 25 OFFSET ?'
        params.append(offset)
        results_list = sql_worker_execution_function(base_query, tuple(params))
    else:
        results_list = sql_worker_execution_function(base_query) 
    results_list = pd.DataFrame(results_list, columns=columns)
    json_str = results_list.to_json(orient='records', date_format='iso')
    return json.loads(json_str) 