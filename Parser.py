# encoding: utf-8
"""
Parser.py
Contains Parser class to download GitHub archives.
"""


from yajl import *
from collections import deque


#TODO: make parser using yajl

class Parser(object):
    """ Parser of JSON archives. """

    def __init__(self, json_file):
        self.json_file = json_file
        self.handler = ContentHandler()
        self.line = deque() #popleft(), append()

    def get_event(self):
        """Returns event from line. If returns None => needs to download new files"""
        if self.line:
            event = self.line.popleft()
            return event
        else:
            return None

class ContentHandler(YajlContentHandler):
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
        self.bracket_stack.pop()