# encoding: utf-8
""" FileSystemWorker.py """

from os import makedirs, path
from json import load, loads
from logging import getLogger


def create_or_check_path(name):
    """Create file or folder if it doesn't exist, else ignore.
    :param name: name of file or folder
    :return True if file or folder exists, else False
    """

    if not path.exists(name):
        if "." in name:
            #it is a file
            open(name, "w").close()
        else:
            #it is a folder
            makedirs(name)
        return False
    return True


def json_file_init(name, to_write):
    """Initialize file in JSON format
    :param name: name of file
    :param to_write: string to write in file
    """

    json_file = open(name, "w")
    json_file.write(to_write)
    json_file.close()


def json_file_load(name):
    """Loads JSON object from file
    :param name: name of JSON file
    :return: Python object
    """

    logger = getLogger('LOGGER')
    json_file = file_open(name)
    if json_file is None:
        return None
    try:
        return load(json_file)
    except ValueError:
        logger.warning(__name__ + ": " + "not a JSON file %s" % name)


def json_string_load(string):
    """Loads JSON object from string
    :param string: JSON string
    :return: Python object
    """
    logger = getLogger('LOGGER')
    try:
        return loads(string)
    except ValueError:
        logger.warning(__name__ + ": " + "not a JSON string %s" % string)


def file_open(name):
    """Opens a file
    :param name: name of file
    :return: file descriptor
    """
    logger = getLogger('LOGGER')
    try:
        return open(name)
    except IOError:
        logger.warning(__name__ + ": " + "no file %s" % name)