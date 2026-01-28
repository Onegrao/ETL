#Code to take the data from raw_data folder and tranfor it into useful information.
import os
import polars as pl
import zipfile

# 1. Config

if not os.path.exists("processed_data"):
    os.makedirs("processed_data")


folder_origin = "raw_data"
files = [f for f in os.listdir(folder_origin) if f.endswith('.zip')] #List all files in the folder that end with .zip
zip_path = os.path.join(folder_origin, files[0]) #Get the full path of the first zip file

bronze_name = os.path.basename(zip_path)
silver_name = bronze_name.replace(".zip", ".csv")
silver_path = os.path.join("processed_data",silver_name) 

#Give title to the columns acording to the data dictionary

entrepeneur_columns = [
    'cnpj_basico', 'razao_social', 'natureza_juridica', 
    'qualificacao_responsavel', 'capital_social', 
    'porte_empresa', 'ente_federativo_responsavel'
]



def transform_data(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_name = z.namelist()[0]

        with z.open(csv_name) as f:
            print(f"Reading data from {csv_name} with Polars...")

            df = pl.read_csv(
                f.read(),
                has_header=False,
                new_columns=entrepeneur_columns,
                sep=';',
                encoding='latin-1',
                truncate_ragged_lines=True
            )

            df = df.with_columns([
                pl.col('capital_social').str.replace(",",".").cast(pl.Float64),
                pl.col('razao_social').str.to_uppercase()
            ])

            return df


print(zip_path)
#df_polars = transform_data(zip_path)
#print(df_polars.head())
#df_polars.write_csv(silver_path)
