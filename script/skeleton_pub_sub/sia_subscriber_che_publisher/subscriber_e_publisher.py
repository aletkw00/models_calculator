import paho.mqtt.client as mqtt
import json

import config
  

#------------------------
# CLASSE PER I PARAMETRI
#
class configurazione_localhost:
    def __init__(self, topic_ricezione_1, topic_ricezione_2, topic_invio_1, topic_invio_2):
        self.dizionario = {"host": "localhost",
                           "porta": 1883,
                           "login": False,
                           "username": "",
                           "password": "",
                           "topic-ricezione-1": topic_ricezione_1,
                           "topic-ricezione-2": topic_ricezione_2,
                           "topic-invio-1": topic_invio_1,
                           "topic-invio-2": topic_invio_2,
                           "cert_tls": ''}
    
    def aggiorna_ad_esterna_login_tls(self, host, username, password, nome_cert):
        self.dizionario.update({"host": host})
        self.dizionario.update({"porta": 8883})
        self.dizionario.update({"login": True})
        self.dizionario.update({"username": username})
        self.dizionario.update({"password": password})
        self.dizionario.update({"cert_tls": nome_cert})

    def get_host(self): 
        return self.dizionario.get('host')
    
    def get_porta(self):
        return int(self.dizionario.get('porta'))

    def get_login(self):
        return bool(self.dizionario.get('login'))

    def get_username(self):
        return self.dizionario.get('username')

    def get_password(self):
        return self.dizionario.get('password')

    def get_topic_ric_1(self):
        return self.dizionario.get('topic-ricezione-1')
        
    def get_topic_ric_2(self):
        return self.dizionario.get('topic-ricezione-2')
    
    def get_topic_inv_1(self):
        return self.dizionario.get('topic-invio-1')
    
    def get_topic_inv_2(self):
        return self.dizionario.get('topic-invio-2')
    
    def get_cert_tls(self):
        return self.dizionario.get('cert_tls')



#-------------------------------------
# FUNZIONE PER LA ELABORAZIONE ALLA RECEZIONE DI UN MESSAGGIO
# L'output deve essere un json/dizionario
#
def elaborazione(msg, topic, par):
    global variabile_globale_1
    global variabile_globale_2
    
    # DEBUG - Stampa tutto il contenuto del messaggio
    # print(msg)
    
    # Converte il messaggio in un json (dizionario)
    msg_json = json.loads(msg)


    # Esegue il dump del json
    nuovo_msg = json.dumps(msg_json)
    
    # TOGLIERE IL COMMENTO PER DEBUG
    # print(nuovo_msg) 
    return nuovo_msg


#----------------------------------
# CLIENT MQTT
# definizione di cosa deve fare alla connessione, iscrizione, ricezione, invio, log
#
def sub_pub_mqtt(par: configurazione_localhost):

    def on_connect(client, userdata, flags, rc):
        # TOGLIERE IL COMMENTO PER DEBUG
        # print(client, userdata, flags, rc)
        pass

    def on_subscribe(client, userdata, mid, granted_qos):
        # TOGLIERE IL COMMENTO PER DEBUG
        # print("message topic=", mid)
        # print("message qos=", granted_qos)
        pass

    def on_message(client, userdata, msg):
        json_string = elaborazione(msg.payload.decode(), msg.topic, par)

        if json_string:  
            client_pub_sub.publish(
                topic=par.get_topic_inv_1(),
                payload=json_string,
                retain=True
            )        

    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    # crea il client per la connessione
    client_pub_sub = mqtt.Client(
        client_id=None,
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport='tcp'
    )

    # callback
    client_pub_sub.on_connect = on_connect  # si può commentare se non interessa
    client_pub_sub.on_subscribe = on_subscribe  # si può commentare se non interessa
    client_pub_sub.on_message = on_message
    # --------------------- 
    # PER DEBUG
    # da commentare per non vedere i log
    #client_pub_sub.on_log = on_log

    # controlla se c'è il login
    if par.get_login():
        client_pub_sub.username_pw_set(par.get_username(), par.get_password())

    # controlla la porta di invio e setta il certificato
    if par.get_porta() != 1883:
        client_pub_sub.tls_set(ca_certs=par.get_cert_tls(), tls_version=2)

    # esegue la connessione al broker
    client_pub_sub.connect(
        host=par.get_host(),
        port=par.get_porta(),
        keepalive=60
    )

    # Iscrizione ai topic di ricezione
    client_pub_sub.subscribe(topic=par.get_topic_ric_1())
    # CI SI PUÒ ISCRIVERE A PIÙ TOPIC
    # client_pub_sub.subscribe(topic=par.get_topic_ric_2())


    # attesa dei messaggi all'infinito, serve per eseguire i callback
    client_pub_sub.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)





#-------------------------------------------
# FUNZIONE MAIN
if __name__ == "__main__":

    # definizione di variabili globali
    global variabile_globale_1
    global variabile_globale_2
    
    variabile_globale_1  = False
    variabile_globale_2 = False
    
    # Connessione al broker e avvio del client mqtt
    parametri = configurazione_localhost(config.TOPIC_RECEIVE_1, config.TOPIC_RECEIVE_2, config.TOPIC_SEND_1, config.TOPIC_SEND_2)
    #
    # togliere il commento per configurazione esterna alla macchina
    #parametri.aggiorna_ad_esterna_login_tls(config.HOST, config.USER, config.PASSWORD, config.CERT_TLS)

    sub_pub_mqtt(parametri)
