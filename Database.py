# encoding: utf-8
""" Database.py """

from DataSaver import DataSaver
from PoolCreator import PoolCreator


class Database(object):
    """	Store of folders and files.	"""

    def __init__(self):
        self.workers = {}
        self.workers_appending()

    def workers_appending(self):
        self.workers["NewData"] = DataSaver()
        self.workers["PoolData"] = PoolCreator()

    def process_data(self, data):
        """ Redirects saving data to special processors
        :param data: data from GitHub event
        """
        return self.workers[data["data_type"]].process_data(data)
