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