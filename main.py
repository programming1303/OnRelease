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


class DataBase(object):
    """
	Main class.
	Stores functions of getting, processing and saving info.
	"""

    def __init__(self):
        from os.path import join
        from time import struct_time

        self.info = {"last_connection_time": struct_time((2014, 5, 1, 0, 0, 0, 3, 127, 0))}

        self.download_dir = "downloads/"
        self.database_dir = "database/"
        self.pool_dir = "pool/"
        self.new_data_dir = "data/"
        self.info_dir = "info/"
        self.data_file = join(self.database_dir, "pairs.json")
        self.info_file = join(self.info_dir, "info.json")
        self.repo_id_file = join(self.database_dir, "repo_id.json")
        self.user_id_file = join(self.database_dir, "user_id.json")
        self.log_file = open("log.txt", "w")

        self.archive = None
        #archive info from info file
        self.user_id = None

    #users id from user_id file

    def log(self, info):
        """Dump info in log file
		:param info: information to dump
		"""
        self.log_file.write(info + '\n')

    @staticmethod
    def create_or_check_path(name):
        """Create file or folder if it doesn't exist, else ignore.
		:param name: name of file or folder
		:return True if file or folder exists, else False
		"""
        from os import makedirs, path

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
            except KeyError:
                self.log("Broken database info file (missing key \"%s\")." % key)
            except TypeError:
                self.log("Broken database info file (not a dictionary).")

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
        self.create_or_check_path(self.data_file)

        from json import load
        from time import struct_time

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

        self.repo_id = get_ids(self.repo_id_file)
        self.user_id = get_ids(self.user_id_file)

    def download_file(self, name):
        """Download file from GitHub archive.
		:param name: name of GitHub archive in format YYYY-MM-DD-h
		"""
        from urllib import urlretrieve
        from gzip import open as gz_open
        from os.path import join
        from os import remove

        archive_name = name + ".json.gz"
        file_name = join(self.new_data_dir, name + ".json")

        urlretrieve("http://data.githubarchive.org/" + archive_name, filename=join(self.download_dir, archive_name))
        archive = gz_open(join(self.download_dir, archive_name))

        json_file = open(file_name, "w")
        json_file.write(archive.read())

        archive.close()
        json_file.close()

        remove(join(self.download_dir, archive_name))

    def get_data_archives(self):
        """Get information from GitHub server."""

        def time_convert(structure):
            """
			:param structure: tuple representation of time
			:return: GitHub archive time
			"""

            def join_number_to_zero(number):
                """
				:param number: positive int number
				:return: adding number to 0 digit [9 -> 09, etc.]
				"""
                return ("" if number > 9 else "0") + str(number)

            return "%s-%s-%s-%s" % (
                structure.tm_year, join_number_to_zero(structure.tm_mon), join_number_to_zero(structure.tm_mday),
                structure.tm_hour)

        current_time = self.get_time()
        if current_time is None:
            self.log("Can't get time.")
            return False

        from time import mktime, gmtime, timezone

        difference = - 28800  # - 3600 * 8 => - 28800
        #timezone difference in seconds between GMT and west coast of USA

        for download_time in range(int(mktime(self.info["last_connection_time"])) + 3600 - timezone,
                                   current_time - 3600, 3600):
            print "Debug Info: (download_time)", gmtime(download_time)
            self.download_file(time_convert(gmtime(download_time + difference)))
            self.info["last_connection_time"] = gmtime(download_time)

    def get_time(self):
        """
		:return: (current time in seconds since the Epoch) or (None if it's impossible to get time)
		"""
        from socket import gaierror, timeout
        from ntplib import NTPClient

        try:
            client = NTPClient()
            response = client.request('pool.ntp.org')
            current_time = int(response.tx_time)
            return current_time
        except ImportError:
            self.log("ImportError: ntplib package not found.")
        except gaierror:
            self.log("socket.gaierror: host name invalid.")
        except timeout:
            self.log("socket.timeout: no response.")
        except:
            self.log("Unknown error.")

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

    def process_events(self):
        """Parse files in data folder and get Watch Events"""
        from json import loads, load
        from os import listdir, remove
        from os.path import join

        for json_file in listdir(self.new_data_dir):
            text = open(join(self.new_data_dir, json_file))
            for line in text:
                event = loads(line)
                if event["type"] == "WatchEvent":
                    self.process_watch_event(event);
                elif event["type"] == "ReleaseEvent":
                    self.process_release_event(event);
            text.close()
            remove(join(self.new_data_dir, json_file))

    def process_watch_event(self, event):
        """Add Users and Repos to DB"""
        from json import loads, load
        from os.path import join

        event["url"] = event["url"][19:]
        print "Debug Info: (pair)", event["actor"], event["url"]
        repo_id = event["repository"]["id"]  # now id is GitHub repo id
        user_id = self.get_id(self.user_id, event["actor"])
        self.create_or_check_path(join(self.database_dir, str(repo_id) + ".json"))
        data_file = open(join(self.database_dir, str(repo_id) + ".json"), "r+w")
        try:
            user_list = load(data_file)
        except ValueError:
            user_list = []

        user_list.append(user_id)
        self.dump_object(user_list, join(self.database_dir, str(repo_id) + ".json"))
        data_file.close()

    def process_release_event(self, event):
        """Make users pool"""

        from json import loads, load
        from os.path import join

        print "Debug Info -- Forming Pool: (pair)", event["actor"], event["url"][19:], event["created_at"]

        try:
            repo_id = event["repository"]["id"]
        except KeyError:
            self.log("RepoID Error")
            return

        try:
            repo_users = open(join(self.database_dir, str(repo_id) + ".json"))
            repo_users_list = load(repo_users)
        except IOError:
            repo_users_list = []
        except ValueError:
            self.log("ValueError while reading repo_users")
            repo_users_list = []

        for user_id in repo_users_list:
            self.create_or_check_path(join(self.pool_dir, str(user_id) + ".json"))
            pool_file = open(join(self.pool_dir, str(user_id) + ".json"), "r+w")

            try:
                repo_list = load(pool_file)
            except ValueError:
                repo_list = []

            repo_list.append(repo_id)
            self.dump_object(repo_list, join(self.pool_dir, str(user_id) + ".json"))
            pool_file.close()

    @staticmethod
    def dump_object(storage, file_name):
        """Dump storage in file
            : param storage: object
		    :param file_name: JSON file
	    """
        from json import dump

        json_file = open(file_name, "w")
        dump(storage, json_file)


db = DataBase()
db.database_init()
db.get_data_archives()
db.process_events()
db.dump_object(db.repo_id, db.repo_id_file)
db.dump_object(db.user_id, db.user_id_file)
print "Debug Info: (last_connection_time)", db.info["last_connection_time"]
db.info["last_connection_time"] = db.info["last_connection_time"].__getslice__(0, 9)
db.dump_object(db.info, db.info_file)















































#QUEEN 4EVA