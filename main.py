# encoding: utf-8
"""
Main file of the project.
Contains DataBase class.
"""
#TODO: connect the file with others

#let's work with time only in GMT
#let's download archive in an hour it was published on GitHub server
#let's save data in format repository:[subscriber1, subscriber2, etc.]
#let's save repositories and users by id, so, we do need dictionary
#let's save GitHub urls without "https://github.com/" [19:]

from Dispatcher import Dispatcher

Dispatcher().processor()