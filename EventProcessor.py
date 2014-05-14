# encoding: utf-8
"""
Contains EventProcessor class and common methods.
"""

from logging import getLogger

from ReleaseEventProcessor import ReleaseEventProcessor
from WatchEventProcessor import WatchEventProcessor


class EventProcessor(object):
    """ Basic event processor, from which all others are inherited. """

    def __init__(self):
        self.event = None
        self.parsers = {}
        self.parsers_appending()
        self.logger = getLogger('LOGGER')

    def parsers_appending(self):
        """ Creating dictionary [event_type: parser]"""
        self.parsers["WatchEvent"] = WatchEventProcessor()
        self.parsers["ReleaseEvent"] = ReleaseEventProcessor()

    def get_type_of_event(self):
        """
        :return: type of GitHub event if getting event was successful else "UnknownType"
        """
        try:
            return self.event["type"]
        except ValueError:
            self.logger.warning(__name__ + ": " + "Missing type in event %s" % self.event)
            return "UnknownEvent"

    def change_event_url(self):
        """ Removes "https://github.com/" from GitHub event url """
        try:
            self.event["url"] = self.event["url"][19:]
        except ValueError:
            self.logger.warning(__name__ + ": " + "Missing url in event %s" % self.event)

    def process_event(self, event):
        """ Redirects processing of GitHub event to special processor
        :param event: GitHub event
        :return: data if processing was successful else None
        """
        self.event = event

        self.change_event_url()
        event_type = self.get_type_of_event()

        if event_type in self.parsers:
            return self.parsers[event_type].get_data_from_event(event)
        else:
            self.logger.error(__name__ + ": " + "Unknown event type %s" % event_type)
