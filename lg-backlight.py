import os, asyncio

from bscpylgtv import WebOsClient
import asyncio_mqtt as mqtt

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


async def main():
	async with mqtt.Client(MQTT_SERVER, MQTT_PORT, username=MQTT_USER, password=MQTT_PASSWORD, client_id="mqtt-lg-backlight") as client:
		async with client.messages() as messages:
			await client.subscribe(MQTT_PATH)
			async for message in messages:
				print(message.topic, message.payload)
				await set_backlight(message.payload.decode("utf-8"))


if __name__ == '__main__':
	asyncio.run(main())
