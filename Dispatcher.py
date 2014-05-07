"""
Dispather.py
Contains Dispatcher class to control process of working.
"""
from Parser import Parser
from EventProcessor import EventProcessor
from Database import DBData, Database
from Downloader import Downloader


class Dispatcher(object):
    def __init__(self, database, parser):
        self.database = database
        self.parser = parser
        self.cur_event = None
        self.event_proceeder = EventProceeder()
        self.data = DBData()
        self.downloader = Downloader()

    def get_event_from_stream(self):
        """Asks Parser for a new event.
		:param name: name of GitHub archive in format YYYY-MM-DD-h
		"""
        #TODO: make parser, think of how parser will tell us it need to download files
        self.cur_event = self.parser.get_event

    def process_event(self):
        """Sends event to EventProceeder.
		:param name: name of GitHub archive in format YYYY-MM-DD-h
		"""
        self.data = self.event_proceeder.proceed_event(self.cur_event)

    def send_to_database(self):
        """Sends data to database."""
        #TODO: make connections with database
        self.database.send_data(self.data)

    def download(self, name):
        """Sends a request to Downloader.
		:param name: name of GitHub archive in format YYYY-MM-DD-h
		"""
        #TODO: make downloader interface
        #empty


