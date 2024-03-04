<!-- versione del 01-09-2023 -->

# Installazione ed esecuzione del client

## Installazione dei pacchetti per il client
Si verifica che siano installati i seguenti programmi
```bash
#si verifica che python3 sia installato (lo script è stato testato con python 3.6 e 3.11)
python3 --version
#se non è installato si esegue
sudo apt-get install python3
#
#si verifica che pip sia installato
pip --version
#se non è installato si esegue
sudo apt-get python3-pip
```
Poi si installano le librerie necessarie al client
```bash
#si installa il pacchetto per il client
python3 -m pip install paho-mqtt
#se è già si default python3 si esegue solo
pip install paho-mqtt
```

## Esecuzione del client come script
Si apre il terminale nella cartella dello script e si lancia il comando
```bash
python3 client.py
```
I file necessari allo script sono:

| file               | descrizione                                           |
|--------------------|-------------------------------------------------------|
| default-config.ini | file per i parametri di configurazione                |
| log.json           | file per l'ultimo messaggio inviato e l'ultimo errore |
| input.cvs          | file da cui leggere i dati                            |

NOTA: la prima esecuzione crea il file delle configurazioni 'default-conf.ini' 
con i seguenti parametri personalizzabili:

| configurazione | descrizione                                                                                   |
|----------------|-----------------------------------------------------------------------------------------------|
| csv_file       | file di input in formato csv <br> default: Input.csv                                          |
| attesa_secondi | intervallo di tempo di invio tra ogni messaggio <br> default: 900 (15 minuti)                 |
| inizio         | messaggio da cui partire                                                                      |
| log_file       | file in cui viene salvata l'ultima riga letta e se c'è stato un errore <br> default: log.json |
| host           | indirizzo ip o dns del broker <br> default: localhost                                         |
| porta          | porta del broker (1883 non ssl, 8883 ssl)<br> default: 1883                                   |
| login          | booleano per abilitare il login <br> default: False                                           |
| username       | login username                                                                                |
| password       | login password                                                                                |
| topic          | nome del topic <br> default: sensori                                                          |
| cert_tls       | file del certificato per la connessione tls <br> default: (vuoto, da inserire)                |



## Funzionamento del client
- primo step
    - sincronizzazione con l'ora corrente:<br>
        - parte dall'ultimo messaggio inviato e confronta l'ora e minuti<br>
        - invia il messaggio precedente all'ora corrente<br>
        esempio: sono le 16:25 invia il messaggio delle 16:15
    - attende i minuti/secondi restanti rispetto al tempo dato:
        - invia il messaggio nei secondi/minuti indicati
- secondo step
    - loop infinito fino alla fine delle righe del csv

NOTA: a ogni invio viene salvato in un file log in json l'ultima riga inviata

### File di log
Nel file log.json vengono salvati;

| variabile | descrizione                            |
|-----------|----------------------------------------|
| riga      | il numero della riga dell'ultimo invio |
| errore    | se ci sono errori di invio             |

## Altri metodi di esecuzione del client
### Metodo 1 - come figlio di un processo
Si esegue un altro script che lancia il client come un processo figlio indipendente

