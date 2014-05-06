# encoding: utf-8
"""
Database.py
Contains Database class to control storage.
"""

from os.path import join
from os import makedirs, path
from time import struct_time
from json import dump, load


class Database(object):
    """	Store of folders and files.	"""

    def __init__(self):
        self.info = {"last_connection_time": struct_time((2014, 5, 5, 0, 0, 0, 0, 131, 0))}

        self.download_dir = "downloaded_data/"
        self.database_dir = "database/"
        self.pool_dir = "pool/"
        self.new_data_dir = "new_data/"
        self.info_dir = "info/"
        self.info_file = join(self.info_dir, "info.json")
        self.user_id_file = join(self.database_dir, "user_id.json")
        self.log_file = "log.txt"

        self.archive = None
        #archive info from info file
        self.user_id = None

    #users id from user_id file

    def log(self, *args):
        """Dump info in log file
		:param args: information to dump
		"""
        log_file = open(self.log_file, "a")
        for info in args:
            log_file.write(str(info) + '\n')

    @staticmethod
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

    @staticmethod
    def json_file_init(name, to_write):
        """Initialize file in JSON format
		:param name: name of file
		:param to_write: string to write in file
		"""
        json_file = open(name, "w")
        json_file.write(to_write)
        json_file.close()

    def database_init(self):
        """Initialize database (create files, folders)."""

        def get_stored_info(key):
            """
			:param key: name of key of dictionary in stored database info file
			:return: value by key, None if error occurs
			"""
            try:
                return self.archive[key]
            except KeyError as e:
                self.log("Broken database info file (missing key %s)." % e)
            except TypeError as e:
                self.log("Broken database info file (not a dictionary).", e)

        def get_ids(file_name):
            #check json object
            # if not check: init
            # return load
            """Get id dictionary from file with catching errors
			:param file_name: JSON file with id list
			:return: loaded JSON object from file or "[]" if error occurs
			"""
            if self.create_or_check_path(file_name):
                try:
                    obj = load(open(file_name))
                except ValueError:
                    self.log("Broken \"%s\" file (not a JSON object)." % file_name)
                    self.json_file_init(file_name, "{}")
                    obj = load(open(file_name))
            else:
                self.log("Missing \"%s\" file." % file_name)
                self.json_file_init(file_name, "{}")
                obj = load(open(file_name))
            return obj

        self.create_or_check_path(self.download_dir)
        self.create_or_check_path(self.pool_dir)
        self.create_or_check_path(self.database_dir)
        self.create_or_check_path(self.new_data_dir)
        self.create_or_check_path(self.info_dir)

        if self.create_or_check_path(self.info_file):
            try:
                self.archive = load(open(self.info_file))
                last_connection_time = get_stored_info("last_connection_time")
                if last_connection_time is not None:
                    self.info["last_connection_time"] = struct_time(last_connection_time)

            except ValueError:
                self.log("Broken database info file (not a JSON object).")
                self.json_file_init(self.info_file, "{}")
        else:
            self.log("Missing database info file.")
            self.json_file_init(self.info_file, "{}")

        self.user_id = get_ids(self.user_id_file)

    @staticmethod
    def get_id(storage, key):
        """Get or set id for key in storage
		:param storage: dictionary
		:param key: string
		:return: id of key
		"""
        if not key in storage:
            storage[key] = len(storage)
            return len(storage) - 1
        return storage[key]

    @staticmethod
    def dump_object(storage, file_name):
        """Dump storage in file
		:param storage: object
		:param file_name: JSON file
		"""

        json_file = open(file_name, "w")
        dump(storage, json_file)


class DBData:
    """Store data in good for DB format"""
    def __init__(self, datatype):
        self.datatype = datatype
