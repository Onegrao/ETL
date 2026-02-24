#Code to take the data from raw_data folder and tranfor it into useful information.
import os
import polars as pl
import zipfile

# 1. Config

if not os.path.exists("processed_data"):
    os.makedirs("processed_data")

#Give title to the columns acording to the data dictionary

empresas = [
    'cnpj_basico', 'razao_social', 'natureza_juridica', 
    'qualificacao_responsavel', 'capital_social', 
    'porte_empresa', 'ente_federativo_responsavel'
]

estabelecimentos = [
    'cnpj_basico', 'cnpj_ordem', 'cnpj_dv', 'identificador_matriz_filial',
    'nome_fantasia', 'situacao_cadastral', 'data_situacao_cadastral',
    'motivo_situacao_cadastral', 'nome_cidade_exterior', 'pais',
    'data_inicio_atividade', 'cnae_fiscal_principal', 'cnae_fiscal_secundaria',
    'tipo_logradouro', 'logradouro', 'numero', 'complemento', 'bairro',
    'cep', 'uf', 'municipio', 'ddd_1', 'telefone_1', 'ddd_2', 'telefone_2',
    'ddd_fax', 'fax', 'correio_eletronico', 'situacao_especial',
    'data_situacao_especial'
]

motivos = [
    'cnpj_basico', 'opcao_simples', 'data_opcao_simples',
    'data_exclusao_simples', 'opcao_mei', 'data_opcao_mei',
    'data_exclusao_mei'
]

socios = [
    'cnpj_basico', 'identificador_socio', 'nome_socio', 'cnpj_cpf_socio',
    'qualificacao_socio', 'data_entrada_sociedade', 'pais', 'representante_legal',
    'nome_representante_legal', 'qualificacao_representante_legal', 'faixa_etaria'
]

paises = [
    'codigo_pais', 'nome_pais']

municipios = [
    'codigo_municipio', 'nome_municipio'
]

qualificacoes = [
    'codigo_tipo_socio', 'descricao_tipo_socio'
]

naturezas = [
    'codigo_natureza_juridica', 'descricao_natureza_juridica'
]

cnaes = [
    'codigo_cnae', 'descricao_cnae'
]

mapeamento_dicionario = {
   "empresas": empresas,
    "estabelecimentos": estabelecimentos,
    "motivos": motivos,
    "socios": socios,
    "paises": paises,
    "municipios": municipios
}

regras_transformacao = {
    "capital_social": lambda: pl.col("capital_social").str.replace(",", ".").cast(pl.Float64),
    "razao_social": lambda: pl.col("razao_social").str.to_uppercase(),
    "cnpj": lambda: pl.col("cnpj").str.pad_start(14, "0")
}


def transform_data(zip_path, coluna_dicionario):
    with zipfile.ZipFile(zip_path, 'r') as z:
        csv_name = z.namelist()[0]
        print(f"Extracted CSV name: {csv_name}")
        

        with z.open(csv_name) as f:
            print(f"Reading data from {csv_name} with Polars...")

            df = pl.read_csv(
                f.read(),
                has_header=False,
                new_columns=coluna_dicionario,
                separator =';',
                encoding='latin-1',
                truncate_ragged_lines=True,
                infer_schema_length=0,
                ignore_errors=True # Ignore rows that cause errors
            )

            expressoes = [
                regras_transformacao[col]() 
                for col in df.columns 
                if col in regras_transformacao
                ]       
    
            # 3. Only apply transformations if there are any expressions to apply
    return df.with_columns(expressoes) if expressoes else df




folder_origin = "raw_data"
files = [f for f in os.listdir(folder_origin) if f.endswith('.zip')] #List all files in the folder that end with .zip
print(f"Files found for processing: {files}")

for i, file in enumerate(files[:2],1):
    zip_path = os.path.join(folder_origin, file)
    silver_name = os.path.basename(zip_path).replace(".zip", ".csv")
    silver_path = os.path.join("processed_data", silver_name)

    #Verify if the file is already processed
    if os.path.exists(silver_path):
        print(f"File {silver_name} already processed. Skipping...")
        continue

    coluna_dicionario = []
    for key,value in mapeamento_dicionario.items():
        if key in silver_name.lower():
            coluna_dicionario = value
            break

    try:

        print(f"Processing file {i}/{len(files)}: {file}")
        df_transformed = transform_data(zip_path, coluna_dicionario)

        print(f"Transformation complete for {silver_name}. Saving to processed_data folder...")
        df_transformed.write_csv(silver_path, separator=';')

        print(f"File {silver_name} processed and saved successfully.")
    except Exception as e:
        print(f"Error processing file {silver_name}: {e}")
    
print("All files processed.")
            



