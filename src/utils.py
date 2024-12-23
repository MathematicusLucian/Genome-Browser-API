import pandas as pd

def load_file(file_name_with_path, sep='\t', comment='#', names=None):
    df = pd.read_csv(file_name_with_path, low_memory=False, sep=sep, comment=comment, names=names)
    print(f"Loaded file: {file_name_with_path}, number of rows: {len(df)}")
    return df