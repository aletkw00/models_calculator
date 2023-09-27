import json
import paho.mqtt.client as mqtt
import ssl
from reg_class import RegressionModel
from utils import *
from const import *
import os
import pandas as pd

df = pd.DataFrame()
num_mex = 0
Utente = 'alessio'
topic = 'serra'
broker_config = 'config.json'
path = os.path.join(MODEL_DIR, Utente, topic)

def elaborazione(messaggio: dict):

    nuovo_msg = json.dumps(messaggio)

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

    def on_message(client, userdata, msg):
        print(msg.payload.decode())
        global num_mex
        global df
        model_dict = {}
        max_window = 0
        
        #translate the json string in a dict
        data_dict = eval(msg.payload.decode())
        #create a dataframe passing a dict
        df1 = pd.DataFrame(data_dict, index=[num_mex])
        num_mex+=1
        #convert when possible the columns in float type
        for column in df1.columns:
        # Prova a convertire la colonna in float
            try:
                df1[column] = df1[column].astype(float)
            except ValueError:
                pass  # Ignora 
        #delete all columns, timestamp excluded, not of float or int type
        df1.drop([col for col in df1.columns if col != 'Date_Time' and \
                            (not df1[col].dtype==float and not df1[col].dtype== int)], \
                                axis = 1, inplace=True)
        #concat the previous message to the new one
        df = pd.concat([df, df1])
        
        
        for name in os.listdir(path):
            Regr = RegressionModel.json_read(os.path.join(path ,name))
            if max_window < Regr.window:
                max_window = Regr.window
            if Regr.window < num_mex:
                df2 = add_cols(df, Regr.window)
                #prendo solo l'ultima riga del mio dataframe
                df2 = df2.tail(1)
                #prendo solo le colonne di cui ho bisongo
                #df2 = df2.iloc[:,:len(df1.columns)*(Regr.window+1)]
                #creo una nuova istanza del dizionario
                model_dict[name]=Regr.predict(df2)
        json_string = elaborazione(model_dict)
        print(json_string)   
        """client_pub_sub.publish(
            topic=par.get("topic-invio"),
            payload=json_string
            # retain=True
        ) """   
        #il +1 lo metto per far si che ci siano nel mio dataframe salvati sempre max_window messaggi
        #al prossimo messaggio ci saranno max window + 1 e a fine conti verrà eliminato il più vecchio
        if num_mex > max_window+1:
            df = df.drop(df.index[:(num_mex-(max_window+1))])
            df.reset_index(drop=True, inplace=True)
            num_mex = max_window +1
        print('\nnumero messaggi: ', len(df), '\n')

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


def configurazione_esterna_login_tls(json_data):
    par = {}
    par.update({"host": json_data['host']})
    par.update({"porta": 8883})
    par.update({"login": True})
    par.update({"username": json_data['username']})
    par.update({"password": json_data['password']})
    par.update({"topic-ricezione": json_data['topic-ricezione']})
    par.update({"topic-invio": "sensori/modelli"})
    par.update({"cert_tls": "ca-root-cert.crt"})
    return par


if __name__ == "__main__":
    path = os.path.join(MODEL_DIR, Utente, topic, broker_config)
    with open(path) as file:
        json_data = json.load(file)

    parametri = configurazione_esterna_login_tls(json_data)

    subscriber_mqtt(parametri)