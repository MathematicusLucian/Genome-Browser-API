# Genome Browser API

Comparison of ancestry website DNA report with SNPedia data. The major/minor alleles of gene variants, their associated gene, chromosome position, etc..

- A **FastAPI** (Python) server (with **Uvicorn**): provides gene variant data (including patient data combined with SNP pairs data to show health risks.)
- **SQLite3Worker**:
  - This library implements a **thread pool pattern** with **sqlite3** being the desired output. The library creates a queue to manage multiple queries sent to the database. (sqllite3 implementation lacks the ability to safely modify the sqlite3 database with multiple threads outside of the compile time options.) Instead of directly calling the sqlite3 interface, the Sqlite3Worker is called, and it inserts the query into a **Queue**.Queue() object. The queries are processed in the order that they are inserted into the queue (first in, first out). In order to ensure that the multiple threads are managed in the same queue, you will need to pass the same Sqlite3Worker object to each thread.
- **Swagger** documentation.
- **VirtualEnv** Python environment, with **`.env`** files.

## Run

### Dev

**Python Environment (VirtualEnv)**

- Create: `python -m venv genomebrowser`
- Launch environment: `source genomebrowser/bin/activate`
- Delete environment: `deactivate` and `rm -r venv`

**Launch the FastAPI server locally**

`python3 src/main.py` (effectively, unvicorn implementation within is: `python -m uvicorn main:app --reload`)

In your browser, open `http://127.0.0.1:8000/`

## Endpoints

![Endpoint: `load_patient`](./assets/endpoint_load_patient.png)

**Load a Patient Genome**

- `/genome/load_patient/{genome_file_name_with_path}`
- If you provide the string `default` for `genome_file_name_with_path`, it will load the default patient data (`genome_Lilly_Mendel_v4.txt`.)

There are several options:

- **`patients/`**: Retrieves a list of the patients (that have been uploaded to the SQLite database.)
- **`snp_research/`**: Retrieves the SNP Pairs data (from published literature, i.e. SNPedia); the underlying method is called when the Uvicorn FastAPI server is launched.
- **`patient_profile/`**: Retrieves patient id, and patient name.
- **`patient_genome_data/`**: Retrieves patient genotypes (gene varients, and the associated two alleles).
- **`patient_genome_data_expanded/`**: Retrieves patient profile, and their genotypes, joined on `patient_id`.
- **`full_report/`**: Retrieves the `patient_genome_data_expanded`, and published literature (join on `rsid.`)

### Swagger

Browse to: `http://127.0.0.1:8000/docs`

![Swagger](./assets/endpoints_swagger.png)

### Considerations

1. The family tree/ancestry websites (i.e. that provide DNA tests; based on saliva samples), do not always use the same lettering as SNPedia.

2. The family tree/ancestry websites do test for many, but not every gene variant.

### Unit Tests

How to run the tests:

1. Ensure `pytest` is installed in your environment.
2. Run the tests using the command: `pytest tests`

## Testing Details

### Unit Tests

The `test` directory contains `pytest` test cases for the `GenomeBrowser` class methods, which include both positive and negative scenarios, as well as exception handling.

Fixtures:

- `genome_browser`: A pytest fixture to initialise the `GenomeBrowser` instance with mock data.
- Mocking the `patient_genome_df` attribute of the `GenomeBrowser` class to use mock data instead of actual data files.

Test Cases:

1. `test_retrieve_data_by_column_positive`:
   - Positive case: valid column and key.
2. `test_retrieve_data_by_column_positive_another_key`:
   - Positive case: another valid column and key.
3. `test_retrieve_data_by_column_negative_column_not_found`:
   - Negative case: column not found.
4. `test_retrieve_data_by_column_negative_key_not_found`:
   - Negative case: key not found.
5. `test_retrieve_data_by_column_no_genome_data`:
   - Negative case: no genome data loaded.
6. `test_retrieve_data_by_column_invalid_column_type`:
   - Negative case: invalid column type.
7. `test_fetch_gene_variant_positive`:
   - Positive case: valid fetch_gene_variant.
8. `test_fetch_gene_variant_negative_key_not_found`:
   - Negative case: fetch_gene_variant key not found.
9. `test_fetch_gene_variant_invalid_key_type`:
   - Exception handling: invalid key type.

## Data Sources

### Genome

`genome_Lilly_Mendel_v4.txt`

[SNPedia: Lily Mendel](https://www.snpedia.com/index.php/User:Lilly_Mendel)

### SNP Pairs Data

The major/minor alleles of gene variants, their associated gene, chromosome position, etc..

`snp_data.csv`

**Columns:** RSID, Magnitude, Risk, Notes
