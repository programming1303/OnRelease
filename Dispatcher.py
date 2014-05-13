# encoding: utf-8
""" Dispatcher.py """

#from Database import Database
#from EventProcessor import EventProcessor
from logging.config import fileConfig

from Parser import Parser
from Downloader import Downloader
from FileSystemWorker import create_or_check_path


class Dispatcher(object):
    """ Dispatcher class to control process of working. """

    def __init__(self):
        create_or_check_path("config/")
        create_or_check_path("logs/")

        fileConfig('config/logger.conf')

        #self.database = Database()
        self.parser = Parser()
        #self.event_processor = EventProcessor()
        self.downloader = Downloader()

        self.new_data_file = None
        self.new_data = None

    def processor(self):
        """ Process of downloading, parsing and saving information. """
        download_status = True
        while download_status:
            getting_event_status = self.get_event()
            if getting_event_status:
                pass
                #if data is not None:
                #self.send_to_database(data)
                #data = self.process_event(None)
            else:
                download_status = self.download()

    def get_event(self):
        """ Asks Parser for a new event.
        :return: event object if getting event has been successful else None
        """
        self.new_data = self.parser.get_event(self.new_data_file)
        return False if self.new_data is None else True

    def download(self):
        """ Sends a request to Downloader.
        :return: False if downloading failed else True
        """
        self.new_data_file = self.downloader.download_archive()
        return False if self.new_data_file is None else True

    @staticmethod
    def process_event():
        """ Sends event to EventProcessor """
        #data = self.event_processor.process_event(event)
        #TODO: EventProcessor interface
        return None

    @staticmethod
    def send_to_database(data):
        """ Sends data to database.
        :param data: data in DB format.
        """
        #TODO: choose data format
        #TODO: DataBase processor
        #self.database.send_data(self.data)

