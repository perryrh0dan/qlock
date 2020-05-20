import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("cmnd/qlock/#")
    client.subscribe("stat/qlock/#")


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("mqtt", "336699")
client.connect("192.168.0.122", 1883, 60)

client.loop_forever()