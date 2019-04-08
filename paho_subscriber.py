# Finlay Miller 2019
# Raspberry Pi hardware data logging script
# Communication Networks Term Project
#
# Writes data from all channels on an MQTT network to different files.
# To be used with the rest of my MQTT logging scripts.
from datetime import datetime
from pathlib import Path

import paho.mqtt.client as mqtt

master_topic_list = "topics"

# make new folder for messages
dt = str(datetime.now()).split('.')[0]
dt = dt.replace(':', '-')
cwd = str(Path.cwd())
msg_folder = str(Path("/Received Messages"))
received = Path(cwd + msg_folder + '/' + dt)
received.mkdir(parents=True, exist_ok=True)


def write_data(message):
	"""
	Updates subscriber-side log files.

	:param message: message to write to output file. Provides both the filename and the data to write
	:return: 		None
	"""
	filename = str(message.topic).replace('/', '-') + '.txt'
	msg = message.payload.decode("utf-8") + '\n'
	with open(received / filename, 'a') as f:
		f.write(msg)
	f.close()


def on_message(client, obj, message):
	"""
	Defines what the paho client should do when it receives a message.

	:param client: 	paho client object
	:param obj: 	not used
	:param message: message received
	:return: 		None
	"""
	print("Message from '{:15}': {}".format(message.topic, str(message.payload.decode("utf-8"))))

	if message.topic == master_topic_list:
		new_topic = message.payload.decode("utf-8")
		client.subscribe(new_topic)
	else:
		write_data(message)


def on_subscribe(client, obj, message):
	"""
	Defines what the paho client should do when it subscribes to a channel successfully

	:param client: 	paho client object
	:param obj: 	not used
	:param message: message received
	:return: 		None
	"""
	print("Subscribing to: " + message)


def main():
	"""
	Create paho client subscriber, listen for messages, and write them to logfiles.

	:return:	None
	"""
	mqtt_server = "localhost"

	print("Creating new instance...")
	client = mqtt.Client("Subscriber1")
	client.on_message = on_message
	client.on_subscribe = on_subscribe
	print("Connecting to broker...")
	client.connect(mqtt_server)
	client.subscribe(master_topic_list)
	client.loop_forever()


if __name__ == '__main__':
	main()
