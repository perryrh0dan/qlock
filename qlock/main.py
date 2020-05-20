import paho.mqtt.client as mqtt
import threading

import clock
from config import getConfig

name = 'Main'
active = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("cmnd/qlock/#")
    client.subscribe("stat/qlock/#")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if topic == 'cmnd/qlock/POWER':
        if payload == 'ON':
            global active
            active = True
        elif payload == 'OFF':
            active = False
    elif topic == 'stat/qlock/POWER':
        print(msg)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    config = getConfig()["mqtt"]
    client.username_pw_set(config["user"], config["password"])
    client.connect(config["host"], config["port"], 60)

    clock = threading.Thread(target=clock.run, args=active)

    client.loop_forever()
