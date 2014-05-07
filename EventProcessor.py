# encoding: utf-8
"""
EventProcessor.py
Contains EventProceeder class and common methods.
"""

from Database import DBData

class EventProcessor(object):
    """ Basic event handling, from which all others are inherited.
    """

    def __init__(self, event):
        """
        :param event: GitHubEvent
        """
        self.event = event
        #TODO: write processor

    def event_type(self):
        #TODO: write typer
        type = None
        return type

class WatchEventProcessor(EventProceeder):
    """ Watch event handling. """
    def process_event(self):

        #TODO: develop watch event processor

class ReleaseEventProcessor(EventProceeder):
    """ Release event handling. """
    def process_event(self):

        #TODO: develop release event processor