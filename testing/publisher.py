import csv
import json
import time
import paho.mqtt.client as mqtt
import sys
import time

client = mqtt.Client()

if client.connect('localhost', 1883, 60) != 0:
    print('not connected to MQTT Broker!1!')
    sys.exit(-1) 

with open('Useful_Data/Input.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        l=json.dumps(row)
        client.publish('test/stauts', l)
        print(l)
        time.sleep(8)

client.disconnect()