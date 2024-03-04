import paho.mqtt.client as mqtt

import config
  

#------------------------
# CLASSE PER I PARAMETRI
#
class configurazione_localhost:
    def __init__(self, topic_invio_1, topic_invio_2):
        self.dizionario = {"host": "localhost",
                           "porta": 1883,
                           "login": False,
                           "username": "",
                           "password": "",
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
    
    def get_topic_inv_1(self):
        return self.dizionario.get('topic-invio-1')
    
    def get_topic_inv_2(self):
        return self.dizionario.get('topic-invio-2')
    
    def get_cert_tls(self):
        return self.dizionario.get('cert_tls')




#----------------------------------
# CLIENT MQTT
# definizione di cosa deve fare alla connessione, invio, log
#
def publisher_mqtt(par: configurazione_localhost, my_message: str):

    def on_connect(client, userdata, flags, rc):
        # TOGLIERE IL COMMENTO PER DEBUG
        # print(client, userdata, flags, rc)
        pass

    def on_publish(client, userdata, mid):
        # TOGLIERE IL COMMENTO PER DEBUG
        # print("message topic=", mid)
        pass
            
    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    # crea il client per la connessione
    client_pub = mqtt.Client(
        client_id=None,
        clean_session=True,
        userdata=None,
        protocol=mqtt.MQTTv311,
        transport='tcp'
    )

    # callback
    client_pub.on_connect = on_connect  # si può commentare se non interessa
    client_pub.on_publish = on_publish  # si può commentare se non interessa
    # --------------------- 
    # PER DEBUG
    # da commentare per non vedere i log
    #client_pub.on_log = on_log

    # controlla se c'è il login
    if par.get_login():
        client_pub.username_pw_set(par.get_username(), par.get_password())

    # controlla la porta di invio e setta il certificato
    if par.get_porta() != 1883:
        client_pub.tls_set(ca_certs=par.get_cert_tls(), tls_version=2)

    # esegue la connessione al broker
    client_pub.connect(
        host=par.get_host(),
        port=par.get_porta()
    )

    # Invia al topic 1
    client_pub.publish(
        topic=par.get_topic_inv_1(),
        payload=my_message,
        retain=True
    )

    # Invia al topic 2
    #client_pub.publish(
    #    topic=par.get_topic_inv_2(),
    #    payload=my_message,
    #    retain=True
    #)


    # chiude la connessione
    client_pub.disconnect()




#-------------------------------------------
# FUNZIONE MAIN
if __name__ == "__main__":

    message = 'Testo di prova'
    
    # Connessione al broker e avvio del client mqtt
    parametri = configurazione_localhost(config.TOPIC_SEND_1, config.TOPIC_SEND_2)
    #
    # togliere il commento per configurazione esterna alla macchina
    #parametri.aggiorna_ad_esterna_login_tls(config.HOST, config.USER, config.PASSWORD, config.CERT_TLS)

    publisher_mqtt(parametri, message)
