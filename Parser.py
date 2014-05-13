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


'''class ContentHandler(YajlContentHandler):
    def __init__(self):
        self.bracket_stack = deque() #append(), pop()
        self.event = None
        self.cur_field = None

    def parse_start(self):
        self.event = {}

    def yajl_null(self, ctx): #can be a dict data
        self.out.write("null\n" )

    def yajl_boolean(self, ctx, boolVal): #can be a dic data
        self.out.write("bool: %s\n" %('true' if boolVal else 'false'))

    def yajl_number(self, ctx, stringNum): #can be a dict data
        #TODO: develop...
        num = float(stringNum) if '.' in stringNum else int(stringNum)
        self.out.write("number: %s\n" %num)

    def yajl_string(self, ctx, stringVal):
        #TODO: develop...
        self.out.write("string: '%s'\n" %stringVal)

    def yajl_start_map(self, ctx):
        self.bracket_stack.append('{')

    def yajl_map_key(self, ctx, stringVal):
        self.cur_field = stringVal

    def yajl_end_map(self, ctx):
        self.bracket_stack.pop()
        self.cur_field = None

    def yajl_start_array(self, ctx):
        self.bracket_stack.append('[')

    def yajl_end_array(self, ctx):
        self.bracket_stack.pop()'''