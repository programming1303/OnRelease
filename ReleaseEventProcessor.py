# encoding: utf-8
""" ReleaseEventProcessor.py """

from logging import getLogger


class ReleaseEventProcessor(object):
    """ ReleaseEvent processor. """

    def __init__(self):
        self.logger = getLogger('LOGGER')

    def get_data_from_event(self, event):
        """ Gets necessary data from GitHub WatchEvent
        :param event: GitHub event
        :return: data for database
        """
        data = {"actor": None, "url": None}
        for key in data.keys():
            try:
                data[key] = event[key]
            except ValueError:
                self.logger.warning(__name__ + ": " + "Missing key %s in event %s" % (key, event))
        return data