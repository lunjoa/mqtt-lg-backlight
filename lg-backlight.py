from bscpylgtv import WebOsClient
import paho.mqtt.client as mqtt

import subprocess, os, asyncio

MQTT_SERVER = os.environ['MQTT_SERVER']
MQTT_PORT = int(os.environ['MQTT_PORT'])
MQTT_USER = os.environ['MQTT_USER']
MQTT_PASSWORD = os.environ['MQTT_PASSWORD']
TV_IP = os.environ['TV_IP']

MQTT_PATH = "home-assistant/lg_brightness/#"

async def set_backlight(backlight):
    client = await WebOsClient.create(TV_IP)
    await client.disconnect()
    await client.connect()

    await client.set_current_picture_settings({"backlight": int(backlight)})
    await client.disconnect()

class Listener:
    def __init__(self):
        print(MQTT_SERVER)
        print(MQTT_PORT)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
        self.client.connect(MQTT_SERVER, MQTT_PORT, 60)
        self.client.loop_forever()
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(MQTT_PATH)

    def on_message(self, client, userdata, msg):
        print(msg.topic + " PAYLOAD: " + msg.payload.decode("utf-8"))
        asyncio.run(set_backlight(msg.payload.decode("utf-8")))

listener = Listener()