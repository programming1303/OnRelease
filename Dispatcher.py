# encoding: utf-8
""" Dispatcher.py """

#from Database import Database
#from Parser import Parser
#from EventProcessor import EventProcessor
from Downloader import Downloader
from FileSystemWorker import create_or_check_path


class Dispatcher(object):
    """ Dispatcher class to control process of working. """

    def __init__(self):
        create_or_check_path("config/")

        #self.database = Database()
        #self.parser = Parser()
        #self.event_processor = EventProcessor()
        self.downloader = Downloader()

        self.new_data = None

    def processor(self):
        """ Process of downloading, parsing and saving information. """
        if True:  # self.parser.is_stream_empty():
            if self.download() is None:
                return
            self.parser.get_event(self.new_data)


    def get_event_from_stream(self):
        """ Asks Parser for a new event. """
        #TODO: make parser, think of how parser will tell us it need to download files
        self.cur_event = self.parser.get_event()

    def process_event(self):
        """ Sends event to EventProceeder. """
        self.data = self.event_processor.proceed_event(self.cur_event)

    def send_to_database(self):
        """ Sends data to database."""
        #TODO: make connections with database
        self.database.send_data(self.data)

    def download(self):
        """ Sends a request to Downloader.
        :return: None if downloading failed else True
        """
        #TODO: make downloader interface
        self.new_data = self.downloader.download_archive()
        return None if self.new_data is None else True


