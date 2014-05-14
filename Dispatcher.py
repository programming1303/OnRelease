# encoding: utf-8
""" Dispatcher.py """

from logging.config import fileConfig
from FileSystemWorker import create_or_check_path
from Database import Database
from EventProcessor import EventProcessor
from Parser import Parser
from Downloader import Downloader


class Dispatcher(object):
    """ Dispatcher class to control process of working. """

    def __init__(self):
        create_or_check_path("config/")
        create_or_check_path("logs/")

        fileConfig('config/logger.conf')

        self.database = Database()
        self.parser = Parser()
        self.event_processor = EventProcessor()
        self.downloader = Downloader()

        self.new_events_file = None
        self.new_data = None
        self.new_event = None

    def processor(self):
        """ Process of downloading, parsing and saving information. """
        download_status = True
        while download_status:
            getting_event_status = self.get_event()
            if getting_event_status:
                processing_event_status = self.process_event()
            else:
                download_status = self.download()

    def get_event(self):
        """ Asks Parser for a new event.
        :return: False if getting event failed else True
        """
        self.new_event = self.parser.get_event(self.new_events_file)
        return False if self.new_event is None else True

    def download(self):
        """ Sends a request to Downloader.
        :return: False if downloading failed else True
        """
        self.new_events_file = self.downloader.download_archive()
        return False if self.new_events_file is None else True

    def process_event(self):
        """ Asks EventProcessor to get data from event.
        :return: False if processing event failed else True
        """
        self.new_data = self.event_processor.process_event(self.new_event)
        return False if self.new_data is None else True

    def save_data(self):
        """ Sends data to Database. """
        #TODO: choose data format
        #TODO: DataBase processor
        self.database.save_data(self.data)
