import csv
import datetime
import time
import pytz

"""
Parte lettura, sincronizzazione dei messaggi
"""


def attesa_sincronizzazione(secondi: int):
    """
    Funzione per l'invio sincronizzato (non precisa) con l'ora e minuti corrente
    """
    timezone_roma = datetime.datetime.now(pytz.timezone('Europe/Rome'))
    if secondi <= 60:
        secondi_restanti = timezone_roma.second % secondi
        time.sleep(abs(secondi - secondi_restanti))
    else:
        minuti_restanti = (timezone_roma.minute * 60) % secondi
        secondi_restanti = minuti_restanti + timezone_roma.second
        time.sleep(abs(secondi - secondi_restanti))


class Messaggi:

    def __init__(self, file: str):
        self.file = file
        self.list_msg = []
        self.workList_msg = []
        self.indice_ultimo_mess_avvio = None

    def csv_to_json(self):
        """
        Funzione che legge il file csv e crea gli elementi in formato json
        """
        # legge csv file
        with open(self.file, encoding='utf-8') as f:
            # carica i dati come un dizionario
            csv_reader = csv.DictReader(f)

            # converte ogni riga csv in un dizionario
            for row in csv_reader:
                # aggiunge la riga in un array
                self.list_msg.append(row)

    def elimina_inizio(self, righe):
        self.workList_msg = self.list_msg[righe:]

    def reset(self):
        self.workList_msg = self.list_msg

    def controllo_se_fine(self):
        if len(self.workList_msg) < 100:
            Messaggi.reset(self)
            return True
        return False

    def sincronizza_ora(self):
        """
        Funzione che salta messaggi confrontando l'ora
        """
        timezone_roma = datetime.datetime.now(pytz.timezone('Europe/Rome'))
        # print(timezone_roma)
        # tempo_corrente = time.localtime()
        righe_saltare = 0
        minuti_totali_correnti = (timezone_roma.hour * 60) + timezone_roma.minute
        # controllo che l'ultimo messaggio sia prima dell'ora e dei minuti
        for msg in self.workList_msg:
            msg_tempo_str = msg.get("Date_Time")
            msg_tempo = time.strptime(msg_tempo_str, "%d/%m/%Y %H:%M")
            if msg_tempo.tm_hour > timezone_roma.hour or msg_tempo.tm_min > timezone_roma.minute:
                righe_saltare = righe_saltare + 1
            else:
                break
        # cerco il messaggio appena prima dell'ora attuale
        for msg in self.workList_msg[righe_saltare:]:
            msg_tempo_str = msg.get("Date_Time")
            msg_tempo = time.strptime(msg_tempo_str, "%d/%m/%Y %H:%M")
            # print(msg_tempo)
            # print(type(msg_tempo))
            # print(tempo_corrente)
            minuti_totali_msg = (msg_tempo.tm_hour * 60) + msg_tempo.tm_min
            if minuti_totali_msg < minuti_totali_correnti:
                righe_saltare = righe_saltare + 1
            else:
                break
        self.indice_ultimo_mess_avvio = righe_saltare - 1
        return self.indice_ultimo_mess_avvio >= len(self.list_msg)

    def get_ultimo_messaggio_avvio(self):
        return self.indice_ultimo_mess_avvio

    def get_work_list(self):
        return self.workList_msg[self.indice_ultimo_mess_avvio:]

