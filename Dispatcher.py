# encoding: utf-8
""" Dispatcher.py """

#from Database import Database
#from Parser import Parser
#from EventProcessor import EventProcessor
from Downloader import Downloader
from FileSystemWorker import create_or_check_path
from logging.config import fileConfig


class Dispatcher(object):
    """ Dispatcher class to control process of working. """

    def __init__(self):
        create_or_check_path("config/")
        create_or_check_path("logs/")

        fileConfig('config/logger.conf')

        #self.database = Database()
        #self.parser = Parser(downloaded_file_name)
        #self.event_processor = EventProcessor()
        self.downloader = Downloader()

        self.new_data = None

    def processor(self):
        """ Process of downloading, parsing and saving information. """
        download_status = True
        while download_status:
            event = self.get_event()
            if event is None:
                download_status = self.download()
            else:
                data = self.process_event(event)
                if data is not None:
                    self.send_to_database(data)

    def get_event(self):
        """ Asks Parser for a new event.
        :return: event object if getting event has been successful else None
        """
        #TODO: parser interface
        return None

    def download(self):
        """ Sends a request to Downloader.
        :return: False if downloading failed else True
        """
        self.new_data = self.downloader.download_archive()
        return False if self.new_data is None else True

    def process_event(self, event):
        """ Sends event to EventProcessor
        :param event: GitHub event object
        """
        #data = self.event_processor.process_event(event)
        #TODO: EventProcessor interface
        return None

    def send_to_database(self, data):
        """ Sends data to database.
        :param data: data in DB format.
        """
        #TODO: choose data format
        #TODO: DataBase processor
        #self.database.send_data(self.data)

