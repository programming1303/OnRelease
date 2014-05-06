# encoding: utf-8
"""
WatchEvent.py
Contains WatchEvent class to create pair user-repo.
"""

from json import load
from os.path import join

from EventProceeder import EventProceeder

#TODO: refactor code to make sure all event-connected methods are in event proceeder
class WatchEventParser(Event):
	""" Parsing WatchEvent. """

	def process(self, event):
		"""Add pair user-repo to database
		:param event: GitHub event
		"""

		event["url"] = event["url"][19:]
		print "Debug Info: (watch)", event["actor"], event["url"]
		repo_id = event["repository"]["id"]  # now id is GitHub repo id
		user_id = self.database.get_id(self.database.user_id, event["actor"])
		self.database.create_or_check_path(join(self.database.database_dir, str(repo_id) + ".json"))
		data_file = open(join(self.database.database_dir, str(repo_id) + ".json"), "r+w")
		try:
			user_list = load(data_file)
		except ValueError:
			user_list = []

		user_list.append(user_id)
		self.database.dump_object(user_list, join(self.database.database_dir, str(repo_id) + ".json"))
		data_file.close()
