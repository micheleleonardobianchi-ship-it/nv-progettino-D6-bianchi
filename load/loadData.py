
from logger_config import Logger
import pandas as pd
from sqlalchemy import create_engine, text
import time
from datetime import datetime
import os
import sys

base_folder = 'data'
subfolder_clean = os.path.join(base_folder, 'clean')
subfolder_log = os.path.join(base_folder, 'log')
os.makedirs(subfolder_log, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(subfolder_log, f"log_load_{timestamp}.txt")
sys.stdout = Logger(log_path)
sys.stderr = Logger(log_path)

# Configurazione via environment variable
DB_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@db:5432/mydatabase')
engine = create_engine(DB_URL)

def load_csv_files():

    # Attendi che il database sia pronto per le connessioni
    time.sleep(5) 

    for file in os.listdir(subfolder_clean):
        if file.endswith('.csv'):

            table_name = 'tdata'
            file_path = os.path.join(subfolder_clean, file)
            
            print(f"Caricamento di {file}...")
            df = pd.read_csv(file_path)
            df['timestamp_load'] = timestamp

            with engine.begin() as connection:
                df.to_sql(
                    name=table_name, 
                    con=connection, 
                    if_exists='append', 
                    index=False
                )
            print(f"Successo: {table_name} creata/aggiornata.")

if __name__ == "__main__":
    load_csv_files()


