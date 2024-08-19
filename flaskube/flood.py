import requests
import concurrent.futures  
import argparse 
import json  
import time  
from datetime import datetime  

# Crea un parser per gli argomenti da linea di comando con una descrizione del programma
parser = argparse.ArgumentParser(description='Send parallel HTTP requests.')

# Aggiunge un argomento obbligatorio che rappresenta l'URL a cui inviare le richieste
parser.add_argument('url', type=str, help='URL to send requests to')

# Aggiunge un argomento opzionale per il numero di worker (thread) da utilizzare, di default è 4
parser.add_argument('--workers', type=int, default=4, help='Number of workers (default: 4)')

# Aggiunge un argomento opzionale per il numero di richieste da inviare, di default è 20
parser.add_argument('--requests', type=int, default=20, help='Number of requests (default: 20)')

# Aggiunge un argomento opzionale per specificare un ritardo tra le richieste, di default è 0 secondi
parser.add_argument('--delay', type=float, default=0, help='Delay between requests in seconds (default: 0)')

# Analizza gli argomenti passati da linea di comando e li memorizza in 'args'
args = parser.parse_args()

# Estrae i valori degli argomenti e li assegna a variabili locali
url = args.url  # URL a cui inviare le richieste
num_workers = args.workers  # Numero di thread da utilizzare per inviare le richieste
num_requests = args.requests  # Numero di richieste totali da inviare
delay = args.delay  # Ritardo tra le richieste

# Definisce la funzione che invia una singola richiesta HTTP GET
def send_request(url):
    time.sleep(delay)  # Introduce un ritardo (se specificato) prima di inviare la richiesta
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Ottiene il timestamp corrente in formato leggibile
    response = requests.get(url)  # Invia una richiesta HTTP GET all'URL specificato
    if response.status_code == 200:  # Controlla se la risposta HTTP ha uno status code 200 (OK)
        print(f"[{timestamp}] {response.content.decode('utf-8')}")  # Stampa il contenuto della risposta con timestamp
    else:
        print(f"[{timestamp}] Error: {response.status_code}")  # Stampa un messaggio di errore con il codice di stato

# Crea un ThreadPoolExecutor per gestire le richieste parallele con il numero di worker specificato
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    futures = []  # Inizializza una lista per tenere traccia delle future esecuzioni
    for i in range(num_requests):  # Ciclo che si ripete per il numero di richieste specificato
        # Invia una richiesta usando un thread del pool e aggiunge la future risultante alla lista
        futures.append(executor.submit(send_request, url))