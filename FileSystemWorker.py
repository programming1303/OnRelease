# encoding: utf-8
""" FileSystemWorker.py """

from os import makedirs, path
from json import load
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
    :param name: name of file
    :return: Python object
    """
    logger = getLogger('LOGGER')
    try:
        json_file = open(name)
        return load(json_file)
    except IOError:
        logger.warning(__name__ + ": " + "no file %s" % name)
    except ValueError:
        logger.warning(__name__ + ": " + "not a JSON file %s" % name)


