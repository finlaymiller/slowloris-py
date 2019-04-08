# Finlay Miller 2019
# Apache data logging script
# Communication Networks Term Project
#
# Searches default Apache 2.4 access and error log folder, extracts all access logs, and formats them nicely
# To be used with the rest of my MQTT logging scripts.
import gzip
import re
from pathlib import Path


def get_files(path):
	"""
	Open all files within a directory.

	:param path: Path to files. Will have file information attached to end.
					 e.g. '~/*.txt'
	:return: Generator for open file objects.
	"""
	for p in path:
		if p.suffix == '.gz':
			yield gzip.open(p, 'rt')
		else:
			yield open(p, 'rt')
		print("File read from: ", str(p))


def concat(sources):
	"""
	Concatenate items from multiple sources into a sequence of items.

	:param sources: Any list object.
	:return: Generator for the objects in said list.
	"""
	for src in sources:
		yield from src


def remap(dctn, name, func):
	"""
	Convert dictionary fields to proper values for a sequence of dictionaries.

	:param dctn:    Dictionary to search in.
	:param name:    Name (or key) of field to remap.
	:param func:    Remapping function to apply.
	:return:        Dictionaries with fields corrected.
	"""
	for field in dctn:
		field[name] = func(field[name])
		yield field


def get_lines(filename, filepath):
	"""
	Extract all lines from all log files within a certain directory.

	:param filename: Name of file to extract data from. Supports wildcards.
	:param filepath: Path to search.
	:return: All lines of all logs in a list.
	"""
	names = Path(filepath).rglob(filename)
	files = get_files(names)
	lines = concat(files)

	return lines


def line_to_log(lines):
	"""
	Convert lines read from file to a list of JSON formatted dictionaries.
	Uses regex to parse lines.

	:param lines: list of lines to convert.
	:return: list of dictionary-formatted logs
	"""
	col_names = ('host', 'identity', 'user', 'datetime',
				 'method', 'request', 'proto', 'status',
				 'bytes', 'referrer', 'user-agent')
	regex_ptn = r'(\S+) (\S+) (\S+) \[(.*?)\] ' \
				r'"(\S+) (\S+) (\S+)" (\S+) (\S+)' \
				r'(\S+) (\S+)'

	# convert to log format
	reg_pat = re.compile(regex_ptn)
	groups = (reg_pat.match(line) for line in lines)
	tuples = (g.groups() for g in groups if g)
	dicts = (dict(zip(col_names, t)) for t in tuples)
	# convert values to proper formats
	log = remap(dicts, "bytes", lambda b: int(b) if b != '-' else 0)
	log = remap(log, "status", int)

	return list(log)


def get_ap_data(input_filename, filepath):
	"""
	Gets all apache access logs in a directory and prints them to a JSON file.
	:return: None.
	"""
	log_lines = get_lines(input_filename, filepath)
	log_list = line_to_log(log_lines)

	return log_list
