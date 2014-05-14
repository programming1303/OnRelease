# encoding: utf-8
"""
Parser.py
Contains Parser class to download GitHub archives.
"""

from logging import getLogger

from FileSystemWorker import file_open, json_string_load


#TODO: make parser using yajl


class Parser(object):
    """ Parser of JSON archives. """

    def __init__(self):
        self.json_file = None
        #self.handler = ContentHandler()
        self.line = None
        self.logger = getLogger('LOGGER')

    def get_event(self, json_file):
        """Returns event from line. If returns None => needs to download new files
        :param json_file: file to read data from
        """
        if json_file is None or self.json_file == json_file:
            if self.json_file is None:
                return None
        else:
            self.json_file = json_file
            self.line = 0

        json_file = file_open(self.json_file)

        if json_file is None:
            self.logger.error(__name__ + ": " + "can't get event from file %s" % self.json_file)
            return None

        for line in range(self.line):
            json_file.readline()

        event = json_string_load(json_file.readline())
        self.line += 1

        if event is None:
            self.logger.error(
                __name__ + ": " + "can't get event from line %d of file %s" % (self.line - 1, self.json_file))
            return None

        return event