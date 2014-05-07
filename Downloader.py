# encoding: utf-8
"""
Downloader.py
Contains Downloader class to download GitHub archives.
"""

from urllib import urlretrieve
from gzip import open as gz_open
from os.path import join
from os import remove
from time import time, gmtime
from FileSystemWorker import create_or_check_path, json_file_load

#TODO: Let's make sure downloader returns None if it has no data to download

class Downloader(object):
    """	Methods of downloading and saving GitHub archives. """

    def __init__(self):
        self.downloaded_data_dir = "downloaded_data/"
        self.new_data_dir = "new_data/"
        self.config_file = join("config/", "downloader.config")

        create_or_check_path(self.downloaded_data_dir)
        create_or_check_path(self.new_data_dir)
        create_or_check_path(self.config_file)

        self.config = self.configuration()

    def configuration(self):
        return json_file_load(self.config_file)

    def download_file(self, name):
        """Download file from GitHub archive.
        :param name: name of GitHub archive in format YYYY-MM-DD-h
        """

        archive_name = name + ".json.gz"
        file_name = join(self.new_data_dir, name + ".json")

        urlretrieve("http://data.githubarchive.org/" + archive_name,
                    filename=join(self.downloaded_data_dir, archive_name))
        archive = gz_open(join(self.downloaded_data_dir, archive_name))

        json_file = open(file_name, "w")
        json_file.write(archive.read())

        archive.close()
        json_file.close()

        remove(join(self.downloaded_data_dir, archive_name))

    def download_archive(self):
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
        print gmtime(current_time)

        if current_time is None:
            self.database.log("Can't get time.")
            return None

        difference = - 28800  # - 3600 * 8 => - 28800
        #timezone difference in seconds between GMT and west coast of USA

        for download_time in range(int(mktime(self.database.info["last_connection_time"])) + 3600 - timezone,
                                   current_time - 3600, 3600):
            print "Debug Info: (download_time)", gmtime(download_time)
            self.download_file(time_convert(gmtime(download_time + difference)))
            self.database.info["last_connection_time"] = gmtime(download_time)

    @staticmethod
    def get_time():
        """
        :return: current time in seconds since the Epoch
        """

        return time()


