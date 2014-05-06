# encoding: utf-8
"""
Downloader.py
Contains Downloader class to download GitHub archives.
"""

from urllib import urlretrieve
from gzip import open as gz_open
from os.path import join
from os import remove
from time import mktime, gmtime, timezone
from socket import gaierror, timeout
from ntplib import NTPClient


class Downloader(object):
	"""	Methods of downloading and saving GitHub archives. """

	def __init__(self, database):
		self.database = database

	def download_file(self, name):
		"""Download file from GitHub archive.
		:param name: name of GitHub archive in format YYYY-MM-DD-h
		"""

		archive_name = name + ".json.gz"
		file_name = join(self.database.new_data_dir, name + ".json")

		urlretrieve("http://data.githubarchive.org/" + archive_name,
		            filename=join(self.database.download_dir, archive_name))
		archive = gz_open(join(self.database.download_dir, archive_name))

		json_file = open(file_name, "w")
		json_file.write(archive.read())

		archive.close()
		json_file.close()

		remove(join(self.database.download_dir, archive_name))

	def get_data_archives(self):
		"""Get information from GitHub server."""

		def time_convert(structure):
			"""
			:param structure: tuple representation of time
			:return: GitHub archive time
			"""

			def join_number_to_zero(number):
				"""
				:param number: positive int number
				:return: adding number to 0 digit [9 -> 09, etc.]
				"""
				return ("" if number > 9 else "0") + str(number)

			return "%s-%s-%s-%s" % (
			structure.tm_year, join_number_to_zero(structure.tm_mon), join_number_to_zero(structure.tm_mday),
			structure.tm_hour)

		current_time = self.get_time()
		if current_time is None:
			self.database.log("Can't get time.")
			return False

		difference = - 28800  # - 3600 * 8 => - 28800
		#timezone difference in seconds between GMT and west coast of USA

		for download_time in range(int(mktime(self.database.info["last_connection_time"])) + 3600 - timezone,
		                           current_time - 3600, 3600):
			print "Debug Info: (download_time)", gmtime(download_time)
			self.download_file(time_convert(gmtime(download_time + difference)))
			self.database.info["last_connection_time"] = gmtime(download_time)

		#TODO: last_connection info in downloader.config

	def get_time(self):
		"""
		:return: (current time in seconds since the Epoch) or (None if it's impossible to get time)
		"""

		try:
			client = NTPClient()
			response = client.request('pool.ntp.org')
			current_time = int(response.tx_time)
			return current_time
		except ImportError as e:
			self.database.log("ImportError: ntplib package not found.", e)
		except gaierror as e:
			self.database.log("socket.gaierror: host name invalid.", e)
		except timeout as e:
			self.database.log("socket.timeout: no response.", e)
		except:
			self.database.log("Unknown error.")


