# encoding: utf-8
"""
Main file of the project.
Contains DataBase class.
"""

#let's work with time only in GMT
#let's download archive in an hour it was published on GitHub server
#let's save data in format repository:[subscriber1, subscriber2, etc.]
#let's save repositories and users by id, so, we do need dictionary
#let's save GitHub urls without "https://github.com/" [19:]

from Database import Database
from Downloader import Downloader
from Parser import Parser

db = Database()
downloader = Downloader(db)
parser = Parser(db)

from time import localtime
db.log("Running " + str(localtime()))

db.database_init()
downloader.get_data_archives()
parser.process_events()
db.dump_object(db.user_id, db.user_id_file)

db.dump_object(db.info, db.info["last_connection_time"].__getslice__(0, 9))

db.log("Finished", "\n")