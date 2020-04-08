from typing import List
from detector.CodebaseReader import CodebaseReader
from datasketch import MinHashLSH
# from detector.clone.CloneDetector import CloneDetector
# from detector.index.CloneIndex import CloneIndex


class ChangesHandler:

    def __init__(self, lsh_index, deletes_lst, updates_lst, creates_lst):
        self.lsh_index: MinHashLSH = lsh_index
        self.deletes_lst: List = deletes_lst
        self.updates_lst: List = updates_lst
        self.creates_lst: List = creates_lst

    def handle_changes(self):
        if len(self.deletes_lst) != 0:
            self.files_deletion_handler()
        if len(self.updates_lst) != 0:
            self.files_update_handler()
        if len(self.creates_lst) != 0:
            self.files_creation_handler()

    def files_deletion_handler(self):
        for deleted_filename in self.deletes_lst:
            self.handle_file_deletion(deleted_filename)

    def handle_file_deletion(self, deleted_filename):
        print("handle deletion for ", deleted_filename)

    def files_update_handler(self):
        for updated_filename in self.updates_lst:
            self.handle_file_deletion(updated_filename)
            self.handle_file_creation(updated_filename)

    def files_creation_handler(self):
        for created_filename in self.creates_lst:
            self.handle_file_creation(created_filename)

    def handle_file_creation(self, created_filename):
        print("handle creation for ", created_filename)
