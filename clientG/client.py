import os.path as path
import sys
import time
import json
# import ssl #se certificato è self-signed
import paho.mqtt.client as mqtt

import utility.parser_config as pconfig
import utility.logging as logging
import utility.messaggi as messaggi


def publish_mqtt(par, my_message: str):
    """
    Funzione che pubblica sul mqtt
    """
    # crea il client per l'invio
    invio = mqtt.Client(
        client_id=None
        # clean_session=True,
        # userdata=None,
        # protocol=mqtt.MQTTv311,
        # transport='tcp'
    )

    # se c'è il login
    if par.get_login():
        invio.username_pw_set(par.get_username(), par.get_password())

    # connessione con certificato 8883
    if par.get_porta() != 1883:
        # se è self signed
        # invio.tls_set(ca_certs=par.get("cert_tls"), tls_version=2, cert_reqs=ssl.CERT_NONE)
        # se non è self signed
        invio.tls_set(ca_certs=par.get_cert_tls(), tls_version=2)

    # prova a connettersi al broker
    try:
        # si connette al broker
        invio.connect(
            host=par.get_host(),
            port=par.get_porta()  # default 1883, per tls/ssl 8883
        )
    except Exception as rifiuto:
        return rifiuto

    # invia il messaggio
    risultato = invio.publish(
        topic=par.get_topic(),
        payload=my_message,
        retain=True
    )

    # controlla se è pubblicato
    if not risultato.is_published():
        rit = ['messaggio NON pubblicato nel topic']
    else:
        rit = ['messaggio pubblicato nel topic']

    # chiude la connessione
    invio.disconnect()

    return rit


'''
MAIN
'''
if __name__ == "__main__":

    # file di configurazione client
    file_config = 'default-config.ini'

    # controlla che esista la configurazione
    if not path.exists(file_config):
        pconfig.config_crea(file_config)
        print("creata configurazione nella stessa cartella dello script")
        sys.exit(0)

    # crea la classe dei parametri
    parametri = pconfig.ParserConfig(file_config)
    parametri.config_leggi()

    # PARSER COMANDI DA TERMINALE
    comandi_terminale = pconfig.parser_command_definizione()
    ARGS = comandi_terminale.parse_args()
    parametri.config_terminale(ARGS)
    # print(parametri.dizionario)

    # vede se esiste il file di log
    logs = logging.Log(parametri.get_log_file())
    logs.legge_crea()

    # ritardo per avvio del servizio #################################
    time.sleep(15)  # ###############################################

    # leggo e creo ogni messaggio, li metto in un array
    mess = messaggi.Messaggi(parametri.get_csv_file())
    mess.csv_to_json()

    # elimino i messaggi già letti
    mess.elimina_inizio(logs.get_riga())

    # controllare che non si è già alla fine
    if mess.controllo_se_fine():
        logs.set_riga(0)

    # punto da cui eseguire un loop infinito di invio
    # si deve resettare il contatore riga, e i messaggi letti
    while True:
        # SEZIONE DI SINCRONIZZAZIONE CON L'ORA E I MINUTI CORRENTI
        #
        # salta le righe per mandare il messaggio precedente
        if mess.sincronizza_ora():
            testo = "si saltano troppe righe rispetto al file iniziale"
            logs.errore(testo)
            sys.exit(1)

        logs.set_riga(logs.get_riga() + mess.get_ultimo_messaggio_avvio())

        workArray = mess.get_work_list()

        # SEZIONE DI INVIO DI MESSAGGI OGNI TOT TEMPO
        #
        # ciclo sul array
        # ci deve essere subito 1 invio
        contatore_sincronizzazione = 1
        for message in workArray:
            # print(message)
            # print(type(message))
            # print(json.dumps(message))

            ritorno = publish_mqtt(parametri, json.dumps(message))
            if len(ritorno) > 1:
                logs.errore(ritorno.args)
                sys.exit(1)

            logs.incrementa_riga()
            contatore_sincronizzazione = contatore_sincronizzazione - 1
            # sincronizzazione dell'invio con i minuti
            if contatore_sincronizzazione == 0:
                contatore_sincronizzazione = 20
                messaggi.attesa_sincronizzazione(parametri.get_secondi())
            else:
                # minuti di intervallo
                time.sleep(parametri.get_secondi())

        # reset per ricominciare a inviare dal primo messaggio
        mess.reset()
        logs.set_riga(0)
