# encoding: utf-8
"""
Contains EventProcessor class and common methods.
"""


class EventProcessor(object):
    """ Basic event handling, from which all others are inherited.
    """

    def __init__(self):
        """
        :param event: GitHubEvent
        """
        self.event = None
        #TODO: write processor

    @staticmethod
    def event_type():
        #TODO: write type
        """


        :return:
        """
        event_type = None
        return event_type


class WatchEventProcessor(EventProcessor):
    """ Watch event handling. """

    def process_event(self):
        """


        """
        pass
        #TODO: develop watch event processor


class ReleaseEventProcessor(EventProcessor):
    """ Release event handling. """

    def process_event(self):
        pass
        #TODO: develop release event processor