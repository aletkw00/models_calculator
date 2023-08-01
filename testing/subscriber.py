import paho.mqtt.client as paho
import sys
from reg_class import Regression
from utils import *
import os
import pandas as pd

final_row = list()
num_mex = 0
path = MODEL_DIR + 'Utente_prova/'
def oneMessage(client, userdata, msg):
    global num_mex
    global final_row
    max_window = 0
    
    row = list()
    first_item = True

    for x in msg.payload.decode().split(',') :
        if first_item:   
            row.append(x)
            first_item = False 
            continue

        if x.endswith('\n'):
            x = x[0:-1]
        try:
            row.append((float)(x))
        except:
            continue
    mex_len = len(row)-1

    #se la pipeline non è vuota elimina l'ultimo timestamp
    if final_row:
        final_row.pop(0)
    final_row = row + final_row
    
    num_mex += 1
    df = pd.DataFrame(final_row).T
    df = df.rename(columns={ df.columns[0]: 'timestamps' })
    
    for name in os.listdir(path):
        Regr = Regression.json_read(path + name)
        if max_window < Regr.window:
            max_window = Regr.window
        if Regr.window < num_mex:
            limite = (Regr.window * mex_len) + mex_len + 1
            df1 = df.iloc[:, 0:limite]
            print(name,': ',Regr.predict(df1))

    if num_mex > max_window + 1:
        reduction = (num_mex-(max_window+1))* mex_len
        final_row[-reduction:] = []
        num_mex = max_window + 1 
    print("\nnumero messaggi: ", num_mex, "\n", len(final_row))

client = paho.Client()
client.on_message = oneMessage
if client.connect('localhost', 1883, 60) != 0:
    print('not connected to MQTT Broker!1!')
    sys.exit(-1)    

client.subscribe("test/stauts")
try:
    print('Press CTRL+C to exit...')
    client.loop_forever()

except:
    print('Disconnected from Broker')
client.disconnect()
