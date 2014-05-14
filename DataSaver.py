# encoding: utf-8
""" DataSaver.py """

from os.path import join

from FileSystemWorker import create_or_check_path, file_open


class DataSaver(object):
    """ """

    def __init__(self):
        self.data_dir = "pairs/"
        self.data_file = join(self.data_dir, "pairs.txt")

        create_or_check_path(self.data_dir)
        create_or_check_path(self.data_file)

    def process_data(self, data):
        data_file = file_open(self.data_file, "a")
        data_file.write(data["actor"] + " " + data["url"] + "\n")
