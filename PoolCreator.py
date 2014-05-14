# encoding: utf-8
""" PoolCreator.py """

from os.path import join

from FileSystemWorker import create_or_check_path, file_open


class PoolCreator(object):
    """ """

    def __init__(self):
        self.pool_dir = "pool/"
        self.pool_file = join(self.pool_dir, "pool.txt")

        create_or_check_path(self.pool_dir)
        create_or_check_path(self.pool_file)

    def process_data(self, data):
        pool_file = file_open(self.pool_file, "a")
        #TODO: common file storage
        data_file = file_open("pairs/pairs.txt")
        for line in data_file:
            pair = line.rstrip().split(" ")
            if pair[1] == data["repository"]:
                pool_file.write(pair[0] + " " + pair[1] + "\n")
