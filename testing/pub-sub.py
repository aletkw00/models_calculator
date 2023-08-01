import ssl
import time
import paho.mqtt.client as mqtt



def elaborazione(messaggio: str):

    nuovo_msg = messaggio + 'elaborato'

    return nuovo_msg


def subscriber_mqtt(par: dict):
    """
    funzione che riceve dall'mqtt
    """

    def on_connect(client, userdata, flags, rc):
        # print(client, userdata, flags, rc)
        pass

    def on_subscribe(client, userdata, mid, granted_qos):
        # print("message topic=", mid)
        # print("message qos=", granted_qos)
        pass

    def on_message(client, userdata, message):
        # print("message received ", str(message.payload.decode("utf-8")))
        # print("message topic=", message.topic)
        # print("message qos=", message.qos)
        # print("message retain flag=", message.retain)

        risultato_elaborazione = elaborazione(str(message.payload.decode("utf-8")))

        # pubblica una stringa, anche se in formato json
        client_pub_sub.publish(
            topic=par.get("topic-invio"),
            payload=risultato_elaborazione
            # retain=True
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
    client_pub_sub.on_log = on_log  # da commentare per non vedere i log

    # se c'è il login
    if par.get("login"):
        client_pub_sub.username_pw_set(par.get("username"), par.get("password"))

    # quale delle 2 porte
    if par.get("porta") != 1883:
        # se è self signed
        client_pub_sub.tls_set(ca_certs=par.get("cert_tls"), tls_version=2, cert_reqs=ssl.CERT_NONE)
        # se non è self signed
        # client_pub_sub.tls_set(ca_certs=par.get("cert_tls"), tls_version=2)

    client_pub_sub.connect(
        host=par.get("host"),
        port=par.get("porta"),  # default 1883, per tls/ssl 8883
        keepalive=60
    )

    # iscrizione al topic
    client_pub_sub.subscribe(topic=par.get("topic-ricevi"))

    # attesa dei messaggi all'infinito, serve per eseguire i callback
    client_pub_sub.loop_forever(timeout=1.0, max_packets=1, retry_first_connection=False)


def configurazione_localhost():
    par = {}
    par.update({"host": "localhost"})
    par.update({"porta": 1883})
    par.update({"login": False})
    par.update({"topic-ricevi": "prova"})
    par.update({"topic-invio": "prova2"})
    return par


def configurazione_localhost_login():
    par = {}
    par.update({"host": "localhost"})
    par.update({"porta": 1883})
    par.update({"login": True})
    par.update({"username": "homeassistant"})
    par.update({"password": "univr_agri01"})
    par.update({"topic-ricevi": "prova"})
    par.update({"topic-invio": "prova2"})
    return par


def configurazione_esterna_login_tls():
    par = {}
    par.update({"host": "90.147.167.187"})
    par.update({"porta": 8883})
    par.update({"login": True})
    par.update({"username": "homeassistant"})
    par.update({"password": "univr_agri01"})
    par.update({"topic-ricevi": "prova"})
    par.update({"topic-invio": "prova2"})
    par.update({"cert_tls": "ca-root-cert.crt"})
    return par


'''
MAIN
'''
if __name__ == "__main__":

    # parametri = configurazione_localhost()
    # parametri = configurazione_localhost_login()
    parametri = configurazione_esterna_login_tls()

    subscriber_mqtt(parametri)
