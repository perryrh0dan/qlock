import paho.mqtt.client as mqtt
import threading

from clock import Clock
from config import getConfig, setConfig

name = 'Main'
clock = Clock()

def on_connect(client, userdata, flags, rc):
    client.subscribe("cmnd/qlock/#")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if topic == 'cmnd/qlock/POWER':
        if payload == 'ON':
            clock.resume()
            client.publish('stat/qlock/POWER', payload='ON', qos=0, retain=False)
        elif payload == 'OFF':
            clock.stop()
            client.publish('stat/qlock/POWER', payload='OFF', qos=0, retain=False)
    elif topic == 'cmnd/qlock/COLOR':
        clock.pause()
        config = getConfig()
        values = list(map(int, payload.split(',')))
        config["color"] = values
        setConfig(config)
        payload = ','.join(map(str, values)) 
        client.publish('stat/qlock/COLOR', payload=payload, qos=0, retain=False)
        clock.refresh()
        clock.resume()
    elif topic == 'cmnd/qlock/TRANSITION':
        clock.pause()
        config = getConfig()
        config["transition"] = payload
        setConfig(config)
        client.publish('stat/qlock/TRANSITION', payload=payload, qos=0, retain=False)
        clock.refresh()
        clock.resume()

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")


if __name__ == "__main__":
    config = getConfig()

    thread = threading.Thread(target=clock.run)
    thread.start()

    if config["mqtt"]["active"]: 
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        client.username_pw_set(config["mqtt"]["user"], config["mqtt"]["password"])
        client.connect(config["mqtt"]["host"], config["mqtt"]["port"], 60)
        
        # Send initial values
        client.publish('stat/qlock/POWER', payload='ON', qos=0, retain=False)
        payload = ','.join(map(str, config["color"])) 
        client.publish('stat/qlock/COLOR', payload=payload, qos=0, retain=False)
        client.publish('stat/qlock/TRANSITION', payload=config["transition"], qos=0, retain=False)

        client.loop_forever()
