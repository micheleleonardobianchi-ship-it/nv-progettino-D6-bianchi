
from logger_config import Logger
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import sys

base_folder = 'data'
subfolder_raw = os.path.join(base_folder, 'extract')
subfolder_clean = os.path.join(base_folder, 'clean')
os.makedirs(subfolder_clean , exist_ok=True)
subfolder_log = os.path.join(base_folder, 'log')
os.makedirs(subfolder_log, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(subfolder_log, f"log_transform_{timestamp}.txt")
sys.stdout = Logger(log_path)
sys.stderr = Logger(log_path)

files = [f for f in os.listdir(subfolder_raw) if os.path.isfile(os.path.join(subfolder_raw, f))]

df_data = pd.DataFrame()

print('Start transform')

for file in files:
    try:
    
        print(file)
    
        file_path = os.path.join(subfolder_raw, file)

        ISIN = file.split('_')[0]
        date = file.split('_')[1]
        
        try:
            timestamp_extract = (file.split('_')[4] + '_' + file.split('_')[5]).replace('.txt', '')
        except IndexError:
            print(f"Errore: Il timestamp del file è mancante.")
            timestamp_extract = 'missing'
                
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Errore: Il file {file_path} non esiste.")
       
        # initializing substrings
        word1 = "Tipo"
        word2 = "Legenda"

        # getting index of substrings
        idx1 = text.find(word1)
        idx2 = text.find(word2)

        # length of substring 1 is added to get string from next character
        data = text[idx1: idx2]

        # Converting the list to a NumPy array and reshaping it into 5 columns
        reshaped_data = np.array(data.split()[1:]).reshape(-1, 5)

        # Creating a DataFrame with 5 columns
        df = pd.DataFrame(reshaped_data, columns=['time','price','return','quantity','type'])

        df['ISIN'] = ISIN
        df['date'] = date
        df['timestamp_extract'] = timestamp_extract
        df['timestamp_transform'] = timestamp

        df_data = pd.concat([df, df_data])

        print('ISIN: ' + ISIN + ' date: ' + date + ' file: ' + file)

    except Exception as e:
        # Catch any other exceptions
        print(f"{e}")
        break

df_prices = df_data.copy()
df_prices = df_prices.reset_index()

df_prices['price'] = [float(x.replace(',','.')) for x in df_prices['price']]
df_prices['return'] = [float(x.replace(',','.')) for x in df_prices['return']]
df_prices['quantity'] = [float(x.replace('.','')) for x in df_prices['quantity']]
df_prices['time'] = [datetime.strptime(x, "%H.%M.%S").time() for x in df_prices['time']]
    
df_prices.head()

df_prices.to_csv(os.path.join(subfolder_clean, f"data_clean_{timestamp}.csv"))

print('End transform')

