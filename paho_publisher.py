# Finlay Miller 2019
# Raspberry Pi hardware data logging script
# Communication Networks Term Project
#
# Publishes data on Apache server and hardware data from psutil to an MQTT network
# To be used with the rest of my MQTT logging scripts.
import sys
import time
from pathlib import Path

import paho.mqtt.publish as publish

import apache_logging as al
import hardware_logging as hl


def get_paths(input_dict):
	"""
	Get paths from dictionary. get_hardware_data() returns nested dicts. This function converts the keys of the nested
	dicts to filepath-type strings which will later be used as MQTT broadcast channels.

	:param input_dict: 	Dictionary to be worked on
	:return: 			Generator of paths
	"""
	for key, value in input_dict.items():
		if isinstance(value, dict):
			for subkey in get_paths(value):
				yield key + '/' + subkey
		else:
			yield key


def get_vals(input_dict):
	"""
	Get values from nested dictionary, sequentially.

	:param input_dict: 	Nested dictionary to run on (doesnt HAVE to be nested)
	:return: 			Generator of values in said dictionary
	"""
	for key, value in input_dict.items():
		if isinstance(value, dict):
			yield from get_vals(value)
		else:
			yield value


def main(argv):
	"""
	Creates paho client publisher. Collects data and publishes it.

	:param argv: 	Number of seconds to run for
	:return: 		None
	"""
	mqtt_server = "192.168.2.10"  # replace with the IP address of your subscriber
	filepath = Path("/var/log/apache2")  # this is the default location
	mqtt_apache_access = "apache/access"
	mqtt_apache_error = "apache/error"

	# set up length of time to log data for
	if argv:
		time_to_run = int(argv[0])
	else:
		time_to_run = 60

	# broadcast list of channels for subscriber to listen to
	hardware_data = hl.get_hw_data()
	for path in get_paths(hardware_data):
		publish.single("topics", path, hostname=mqtt_server)
	publish.single("topics", mqtt_apache_access, hostname=mqtt_server)
	publish.single("topics", mqtt_apache_error, hostname=mqtt_server)

	# give subscribers a chance to subscribe
	time.sleep(2)

	# log and broadcast hardware data for set length of time
	print("Running for {} seconds".format(time_to_run))
	t0 = time.time()
	while True:
		t1 = time.time()
		hardware_data = hl.get_hw_data()

		for path, val in zip(get_paths(hardware_data), get_vals(hardware_data)):
			publish.single(path, str(val), hostname=mqtt_server)
			print("{:15}: {}".format(path, val))

		if (t1 - t0) > time_to_run:
			break
		time.sleep(1)

	# log and broadcast Apache data. Apache automatically writes all the
	# information we need to files so we don't need to run it in the loop.

	apache_data = al.get_ap_data("access.*", filepath)
	publish.single(mqtt_apache_access, str(apache_data), hostname=mqtt_server)
	apache_data = al.get_ap_data("error.*", filepath)
	publish.single(mqtt_apache_error, str(apache_data), hostname=mqtt_server)


if __name__ == '__main__':
	main(sys.argv[1:])
