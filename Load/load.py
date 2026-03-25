import os
import sqlite3
import polars as pl


def load_data(silver_folder, db_name):
    os.makedirs(os.path.dirname(db_name), exist_ok=True)
    conn = sqlite3.connect(db_name)

    # PRAGMAs de performance
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    files = [f for f in os.listdir(silver_folder) if f.endswith('.csv')]

    if not files:
        print("No CSV files found in the processed_data folder.")
        conn.close()
        return

    for file_name in files:
        table_name = file_name.replace('.csv', '').lower()
        path_file = os.path.join(silver_folder, file_name)

        print(f"Loading data from {path_file} into table {table_name}")

        
        reader = pl.read_csv_batched(
            path_file,
            separator=';',
            batch_size=50000
        )

        i = 0
        while True:
            batches = reader.next_batches(1)
            if not batches:
                break

            for batch in batches:
                batch.write_database(
                    table_name,
                    conn,
                    if_exists='append',
                    index=False
                )

                if i % 10 == 0:
                    print(f"Bloco {i} inserindo")
                i += 1

        print(f"Finished loading data into table {table_name}")

    conn.close()
    print("All data has been loaded into the database.")

def load():  
    print("Starting the loading process...")
    silver_folder = "processed_data"
    db_name = "Load/dadoscnpj.db"       
    load_data(silver_folder, db_name)