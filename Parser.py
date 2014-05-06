# encoding: utf-8
"""
Parser.py
Contains Parser class to download GitHub archives.
"""

from json import loads
from os import listdir, remove
from os.path import join
from WatchEventParser import WatchEventParser
from ReleaseEventParser import ReleaseEventParser


class Parser(object):
	""" Parser of JSON archives. """

	def __init__(self, database):
		self.database = database

	def process_events(self):
		"""Parse files in data folder and get Watch Events"""

		for json_file in listdir(self.database.new_data_dir):
			text = open(join(self.database.new_data_dir, json_file))
			for line in text:
				event = loads(line)
				if event["type"] == "WatchEvent":
					WatchEventParser(self.database).process(event)
				elif event["type"] == "ReleaseEvent":
					ReleaseEventParser(self.database).process(event)
			text.close()
			remove(join(self.database.new_data_dir, json_file))