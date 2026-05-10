
from logger_config import Logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import sys

base_folder = 'data'
subfolder = os.path.join(base_folder, 'extract')
os.makedirs(subfolder, exist_ok=True)
subfolder_log = os.path.join(base_folder, 'log')
os.makedirs(subfolder_log, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_path = os.path.join(subfolder_log, f"log_extract_{timestamp}.txt")
sys.stdout = Logger(log_path)
sys.stderr = Logger(log_path)

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/chromium-browser"

# Selected sample:
# IT0004923998 	Btp Tf 4,75% St44 Eur 
# XS2908645265  Romania Fx 6% Sep44 Eur
   
lISIN = ['IT0004923998',
         'XS2908645265']	

# Inizializza il driver
driver = webdriver.Chrome(options=chrome_options)

for security in range(len(lISIN)):

    ISIN = lISIN[security]

    df_data = pd.DataFrame()
    page_number = 0
    
    url0 = 'https://www.borsaitaliana.it/borsa/obbligazioni/mot/btp/contratti.html?isin=' + ISIN + '&lang=it&page=0'
    
    # Wait for the page to fully load
    time.sleep(np.random.uniform(5, 10))
    
    # Open the webpage
    driver.get(url0)
    
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    text = soup.get_text().replace("\n", " ")
    
    # getting index of substrings
    idx1 = text.find("Numero Contratti:")
    idx2 = text.find("Quantità Totale:")
    idx3 = text.find("Ora ")
    idx4 = text.find("Ultimo Contratto")
    idx5 = text.find("Aggiungi un Email Alert")
    
    contracts_numbers = int(text[idx1:idx2].split()[2].replace('.',''))
    total_quantity = int(text[idx2:idx3].split()[2].replace('.',''))
    trading_day = text[idx4:idx5].split()[2]
    trading_day = datetime.strptime(trading_day, "%d/%m/%y")
    
    print('\n')
    print('ISIN: ' + ISIN)
    print('trading day: ' + str(trading_day))
    print('total quantity: ' + str(total_quantity))
    print('contracts numbers: ' + str(contracts_numbers))
    
    n_pages = int(np.ceil(contracts_numbers/20))
    lpages = list(np.random.permutation(list(range(n_pages))))
    
    print('number of pages: ' + str(n_pages))
    
    for page_number in lpages:
        try:            
            # Wait for the page to fully load
            time.sleep(np.random.uniform(5, 10))

            url = 'https://www.borsaitaliana.it/borsa/obbligazioni/mot/btp/contratti.html?isin=' + ISIN + '&lang=it&page='
            url = url + str(page_number)

            # Open the webpage
            driver.get(url)

            # Parse the page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            text = soup.get_text().replace("\n", " ")

            # Nome file pulito
            data_str = str(trading_day)[0:10].replace('-', '')
            filename = f"{ISIN}_{data_str}_pag_{page_number}_{timestamp}.txt"
            filepath = os.path.join(subfolder, filename)

            # Salvataggio
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
    
            print(f"File salvato: {filepath}")
       
        except Exception as e:
            # Catch any other exceptions
            print(f"{e}")
            break
    
driver.quit()
