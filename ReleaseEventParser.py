# encoding: utf-8
"""
ReleaseEventParser.py
Contains ReleaseEvent class to create users pull.
"""

from json import load
from os.path import join


class ReleaseEventParser():
    """ Parsing ReleaseEvent. """

    def process(self, event):
        """Make users pool
        :param event: GitHub event
        """

        print "Debug Info: (release)", event["actor"], event["url"][19:], event["created_at"]

        try:
            repo_id = event["repository"]["id"]
        except KeyError:
            self.database.log("KeyError: [\"repository\"][\"id\"] in ReleaseEvent.")
            return

        try:
            repo_users = open(join(self.database.database_dir, str(repo_id) + ".json"))
            repo_users_list = load(repo_users)
        except IOError:
            repo_users_list = []
        except ValueError:
            self.database.log("ValueError while reading repo_users")
            repo_users_list = []

        for user_id in repo_users_list:
            self.database.create_or_check_path(join(self.database.pool_dir, str(user_id) + ".json"))
            pool_file = open(join(self.database.pool_dir, str(user_id) + ".json"))

            try:
                repo_list = load(pool_file)
            except ValueError:
                repo_list = []

            repo_list.append(repo_id)
            pool_file.close()
            self.database.dump_object(repo_list, join(self.database.pool_dir, str(user_id) + ".json"))

