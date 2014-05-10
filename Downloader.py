# encoding: utf-8
""" Downloader.py """

from urllib import urlretrieve
from gzip import open as gz_open
from os.path import join
from os import remove
from time import time, gmtime, struct_time
from calendar import timegm
from FileSystemWorker import create_or_check_path, json_file_load
from logging import getLogger


class Downloader(object):
    """	Methods of downloading and saving GitHub archives. """

    def __init__(self):
        self.downloaded_data_dir = "downloaded_data/"
        self.new_data_dir = "new_data/"
        self.config_file = join("config/", "downloader.conf")

        create_or_check_path(self.downloaded_data_dir)
        create_or_check_path(self.new_data_dir)
        create_or_check_path(self.config_file)

        self.config = self.configuration()
        self.logger = getLogger('LOGGER')

    def configuration(self):
        """Invoke downloader configuration.
        :return: configuration from config file if invoking was successful else default configuration
        """
        config = json_file_load(self.config_file)
        default = {"last_connection_time": struct_time((2014, 5, 9, 12, 0, 0, 3, 134, 0))}
        return config or default

    def download_file(self, name):
        """Download file from GitHub archive.
        :param name: name of GitHub archive in format YYYY-MM-DD-h
        :return: name of JSON file with data
        """
        #TODO: handle exceptions
        archive_name = name + ".json.gz"
        file_name = join(self.new_data_dir, name + ".json")

        try:
            urlretrieve("http://data.githubarchive.org/" + archive_name,
                        filename=join(self.downloaded_data_dir, archive_name))
        except IOError:
            self.logger.error("unable to download file (error creating connection).")

        try:
            archive = gz_open(join(self.downloaded_data_dir, archive_name))
        except IOError:
            self.logger.error("unable to open gzipped file (file not created).")
        else:
            json_file = open(file_name, "w")
            json_file.write(archive.read())

            archive.close()
            json_file.close()

            remove(join(self.downloaded_data_dir, archive_name))

            return file_name

    def download_archive(self):
        """Get data from GitHub server.
        :return: name of JSON file with data if downloading was successful else None
        """

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
        self.logger.debug("current time: " + str(gmtime(current_time)))

        difference = -25200
        #timezone difference in seconds between GMT and west coast of USA

        downloading_time = int(timegm(self.config["last_connection_time"])) + 3600
        self.logger.debug("downloading time: " + str(gmtime(downloading_time)))

        if downloading_time > current_time - 7200:
            self.logger.info("unable to download file (time limiting).")
            return

        downloading_time += difference

        json_file_name = self.download_file(time_convert(gmtime(downloading_time)))

        self.config["last_connection_time"] = gmtime(downloading_time - difference)
        self.logger.debug("last_connection_time: " + str(self.config["last_connection_time"]))

        return json_file_name

    @staticmethod
    def get_time():
        """
        :return: current time in seconds since the Epoch
        """

        return int(time())