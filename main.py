import pandas as pd
import re

def load_genome(genome_file_name_with_path):
    df = pd.read_csv(genome_file_name_with_path, sep = '\t', comment='#')
    return df

def main():
    print("Genome Browser")
    genome_file_name_with_path = './data/genomes/genome_Lilly_Mendel_v4.txt'
    df = load_genome(genome_file_name_with_path)
    print(df.size)

if __name__ == "__main__":
    main()