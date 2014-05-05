# encoding: utf-8
"""
Event.py
Contains Event class and common methods.
"""


class Event(object):
	""" Basic event, from which all others inherited. """

	def __init__(self, database):
		self.database = database
