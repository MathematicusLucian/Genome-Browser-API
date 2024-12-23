from venv import logger
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def load_file(file_name_with_path, names=None, straight: bool = False):
    params_list = {'sep': '\t', 'comment': '#', 'names': names}
    params = None
    params = {k: v for k, v in params_list.items() if straight is False} 
    return pd.read_csv(file_name_with_path, low_memory=False, **params) 

def check_if_default(variant_id):
    if variant_id == "default":
        variant_id = "rs10516809"
    return variant_id