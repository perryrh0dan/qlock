import paho.mqtt.client as mqtt
import threading

from clock import Clock
from config import getConfig, setConfig

name = 'Main'
clock = Clock()


def on_connect(client, userdata, flags, rc):
    print(name + ' - Successful connected to mqtt client')
    config = getConfig()
    client.subscribe('cmnd/' + config['mqtt']['topic'] + '/#')


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    config = getConfig()
    if topic == 'cmnd/' + config['mqtt']['topic'] + '/POWER':
        if payload == 'ON':
            clock.resume()
            client.publish('stat/' + config['mqtt']['topic'] + '/POWER', payload='ON',
                           qos=0, retain=False)
        elif payload == 'OFF':
            clock.stop()
            client.publish('stat/' + config['mqtt']['topic'] + '/POWER', payload='OFF',
                           qos=0, retain=False)
    elif topic == 'cmnd/' + config['mqtt']['topic'] + '/COLOR':
        clock.pause()
        values = list(map(int, payload.split(',')))
        config["color"] = values
        setConfig(config)
        payload = ','.join(map(str, values))
        client.publish('stat/' + config['mqtt']['topic'] + '/COLOR', payload=payload,
                       qos=0, retain=False)
        clock.refresh()
        clock.resume()
    elif topic == 'cmnd/' + config['mqtt']['topic'] + '/TRANSITION':
        clock.pause()
        config["transition"] = payload
        setConfig(config)
        client.publish('stat/' + config['mqtt']['topic'] + '/TRANSITION',
                       payload=payload, qos=0, retain=False)
        clock.refresh()
        clock.resume()


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")


if __name__ == "__main__":
    config = getConfig()

    print(name + ' - Start clock in new thread')
    thread = threading.Thread(target=clock.run)
    thread.start()

    if config["mqtt"]["active"] == True:
        print(name + ' - Start mqtt client')
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect

        client.reconnect_delay_set(min_delay=1, max_delay=120)

        client.username_pw_set(
            config["mqtt"]["user"], config["mqtt"]["password"])
        client.connect(config["mqtt"]["host"], config["mqtt"]["port"], 60)

        # Send initial values
        topic = 'stat/' + config['mqtt']['topic'] + '/POWER'
        client.publish(topic, payload='ON', qos=0, retain=False)
        topic = 'stat/' + config['mqtt']['topic'] + '/COLOR'
        payload = ','.join(map(str, config["color"]))
        client.publish(topic, payload=payload, qos=0, retain=False)
        topic = 'stat/' + config['mqtt']['topic'] + '/TRANSITION'
        client.publish(topic, payload=config["transition"], qos=0, retain=False)
        client.loop_forever()
