import paho.mqtt.client as paho
import sys
import time

client = paho.Client()

if client.connect('localhost', 1883, 60) != 0:
    print('not connected to MQTT Broker!1!')
    sys.exit(-1) 

with open('Useful_Data/Input.csv') as f:
    first_line = True
    for l in f:
        if first_line:
            first_line = False
            continue
        client.publish('test/stauts', l)
        print(l)
        time.sleep(8)

client.disconnect()
