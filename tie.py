import paho.mqtt.client as paho
from reg_class import Regression
from utils import *
import os
import pandas as pd
import time

final_row = list()
num_mex = 0
path='jzon/'

def mex(msg):
    global num_mex
    global final_row
    max_window = 0

    timestamps = ''
    row = list()
    first_item = True

    for x in msg.split(',') :
        if first_item:   
            timestamps = x
            first_item = False 
            continue

        if x.endswith('\n'):
            x = x[0:-1]
        try:
            row.append((float)(x))
        except:
            continue
    mex_len = len(row)

    #se la pipeline non è vuota elimina l'ultimo timestamp
    if final_row:
        final_row.pop(0)
    final_row = timestamps + row + final_row
    print(final_row)

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

with open('Useful_Data/Input.csv') as f:
    first_line = True
    for l in f:
        if first_line:
            first_line = False
            continue
        print(l)
        mex(l)
        time.sleep(6)

