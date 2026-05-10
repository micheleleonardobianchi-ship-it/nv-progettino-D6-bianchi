
Corso di *Network Virtualization and Softwarization* 

Master in Data Science per la Pubblica Amministrazione (a.a. 2025/2026, prof. Stefano Salsano).

---

## Progettino

# Mini-stack dati Pipeline ETL a 3 stadi

**Autore:** Michele Leonardo Bianchi

**Codice variante:** D6

**Repo:** https://github.com/micheleleonardobianchi-ship-it/nv-progettino-D6-bianchi

---

## Struttura cartelle

```
.
├── README.md             
├── compose.yaml     
├── dockerfiles/
│   ├── Dockerfile.extract          # Dockerfile separati per servizio
│   ├── Dockerfile.clean
│   ├── Dockerfile.load    
├── logger_config.py                # funzione python per la creazione dei file di log
├── extract/
│   ├── extractData.py              # codice per lo scarico dei dati
│   └── requirements_extract.txt   
├── transform/
│   ├── transformData.py            # codice per la transformazione dei dati 
│   └── requirements_transform.txt  
├── load/
│   ├── loadData.py                 # codice per caricare i dati sul DB
│   └── requirements_load.txt  
├── scripts/
│   ├── setup.sh                    # script per avviare l'esperimento
│   └── teardown.sh                 # script per pulire al termine
├── screenshots/                    # 5 screenshot della demo funzionante
```

---

## 1. Obiettivo

Scaricare le informazioni dal sito di Borsa Italiana relative ai prezzi di alcune obbligazioni (“extract”), transformare i file di testo relativi alle pagine web in un dataframe pandas e quindi in un file .csv (“transform”), caricare i dati su un DB (“load”) che può essere interrogato (“db”). 

---

## 2. Architettura

Tre servizi, un DB e un container di verifica: 

- extract  
- transform 
- load 
- db
- verify

```
+----------------------+     +----------------------+     +--------------+
| extract:             |     | transform:           |     | load_        |  
| scarico in più fasi  | --> | da file di testo,    | --> | carica i     | --> Postgres
| dal sito di          |     | a dataframe pandas   |     | dati nel DB  |        |
| Borsa Italiana       |     |                      |     |              |        |
+----------------------+     +----------------------+     +--------------+        |
           |                            |                         |               |
           |            volume condiviso con sottocartelle        |               |    
           |            extract, clean e log                      |               |     
           |                                                      |               |
                                                                  |   volume db   |
           
              
```

**volume condiviso (dati-app) + volume db (dati-db)**: 

- `extract` genera file `extract/<ISIN>_<trading date>_pag_<N>_<timestamp_extract>.txt`; 
- `transform` legge i files .txt, li trasforma e scrive il file `clean/dati_clean_<timestamp_clean>.csv`; 
- `load` legge da `clean/` e fa `INSERT` su Postgres;
- ciascuno dei tre servizi genera un file di log `log/log_<nome_servizio>_<timestamp_servizio>.txt`; 

---

## 3. Prerequisiti

- Ubuntu 24.04 LTS MATE 1.26.2  
- Docker 29.4.2  

---

## 4. Come riprodurre passo-passo

#### Step 1 — Avviare l’esperimento

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Output atteso:**  

- build delle immagini Docker;
- avvio dei container `extract`, `transform`, `load`, `db`, e `verify`;
- creazione dei Docker volumes condivisi tra i servizi.

#### Step 2 — Verificare i Docker volumes

```bash
docker volume ls
```

**Output atteso:**  
presenza dei volumi Docker utilizzati per:

- file raw estratti;
- file clean trasformati;
- file di log;
- persistenza del database Postgres.

I file creati possono essere cercati e visualizzati utilizzando

```bash
docker volume inspect dati-app
sudo ls /var/lib/docker/volumes/progettino_dati-app/_data
sudo pluma /var/lib/docker/volumes/progettino_dati-app/_data/clean/data_clean_<timestamp>.csv
```

#### Step 3 — Verificare che il DB funzioni

```bash
docker compose exec db psql -U user -d mydatabase
```

eseguendo la query `SELECT count(*) FROM tdata`

**Output atteso:**  
presenza di dati nel DB.


#### Step 4 — Terminare l’esperimento

```bash
chmod +x scripts/teardown.sh
./scripts/teardown.sh
```

**Output atteso:**  

- arresto e rimozione dei container;
- rimozione della rete Docker associata;
- cleanup delle risorse create durante l’esperimento.

---

## 5. Verifica del funzionamento

Si rimanda alla cartella `screenshots`.

---

## 6. Riflessioni e punti aperti

Durante lo sviluppo della pipeline ETL sono emersi diversi aspetti critici legati sia all’architettura sia alla gestione dei dati.

### Gestione dei file e dei nomi
La creazione di sottocartelle semplifica la struttura ma rende più articolata la preparazione degli script. Nel DB il nome delle tavole deve essere in minuscolo (`tdata`) e non in maiuscolo (`TDATA`).

### Orchestrazione dei container
È stato necessario introdurre uno step di verifica nel `compose.yaml` per eseguire la query di test solo dopo la completa esecuzione del container `load`. Questo ha risolto problemi di sincronizzazione tra servizi.

### Scarico dati in più fasi
La suddivisione dello scraping in più file fasi migliorerebbe la gestione del processo: data una obbligazione (ISIN) bisognerebbe prima creare una file in cui raccogliere il numero di pagine da visitare e poi avviare lo scarico dei dati, eventualmente anche utilizzando più container per lo scarico dei dati. 

### Duplicati
È emersa la presenza di dati duplicati dovuta a scarichi, trasformazioni o caricamenti ripetuti (ad esempio, se si avvia `setup.sh` più di una volta). Questo richiederebbe una modifica a livello di gestione di file oppure in fase di inserimento nel DB. Nella presente versione sono riportati nella tavola del DB `tdata` i timestamp relativi a ciscuno dei tre servizi.

Strategie alternative:

- sovrascrittura dei dati (ma si rischia di perdere dati se uno dei volumi viene meno)
- accodamento (storico completo ma richiede controllo duplicati)
- inserimento con controlli in fase di inserimento `load`

---

## 7. Riferimenti

- Guida hands-on Docker su WSL2: `Docker_WSL2_Guida_Esercitazioni.md`




