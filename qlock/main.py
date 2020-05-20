import paho.mqtt.client as mqtt
import threading

from clock import Clock
from config import getConfig

name = 'Main'
clock = Clock()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("cmnd/qlock/#")
    client.subscribe("stat/qlock/#")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if topic == 'cmnd/qlock/POWER':
        if payload == 'ON':
            clock.resume()
            client.publish('stat/qlock/POWER', payload='ON', qos=0, retain=False)
        elif payload == 'OFF':
            clock.pause()
            client.publish('stat/qlock/POWER', payload='OFF', qos=0, retain=False)
    elif topic == 'stat/qlock/POWER':
        print(msg)

if __name__ == "__main__":
    config = getConfig()

    thread = threading.Thread(target=clock.run)
    thread.start()

    if config["mqtt"]["active"]: 
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.username_pw_set(config["mqtt"]["user"], config["mqtt"]["password"])
        client.connect(config["mqtt"]["host"], config["mqtt"]["port"], 60)
        client.loop_forever()
