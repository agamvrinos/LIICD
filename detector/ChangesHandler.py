from typing import List
from detector.CodebaseReader import CodebaseReader
from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex


class ChangesHandler:

    def __init__(self, detector, deletes_lst, updates_lst, creates_lst):
        self.detector: CloneDetector = detector
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
        clone_index: CloneIndex = self.detector.get__clone_index()
        index_entries_by_file = clone_index.get__index_entries_by_file()

        for deleted_filename in self.deletes_lst:
            self.handle_file_deletion(deleted_filename, clone_index, index_entries_by_file)

    def handle_file_deletion(self, deleted_filename, clone_index, index_entries_by_file):
        deleted_index_entries = index_entries_by_file[deleted_filename]

        # detect the clones to be removed
        results = self.detector.detect_clones(deleted_index_entries)
        print("Clones Removed")
        for group in results:
            print(group)

        # remove corresponding entries from the file index (by hash)
        for deleted_entry in deleted_index_entries:
            hash_val = deleted_entry.get__sequence_hash()
            index_entries_by_hash = clone_index.get__index_entries_by_hash()

            entries_lst = index_entries_by_hash[hash_val]
            if len(entries_lst) == 1:
                del index_entries_by_hash[hash_val]
            else:
                entries_lst.remove(deleted_entry)

        # remove corresponding entries from the file index (by filename)
        del index_entries_by_file[deleted_filename]

    def files_update_handler(self):
        clone_index: CloneIndex = self.detector.get__clone_index()
        index_entries_by_file = clone_index.get__index_entries_by_file()

        for updated_filename in self.updates_lst:
            self.handle_file_deletion(updated_filename, clone_index, index_entries_by_file)
            self.handle_file_creation(updated_filename, clone_index)

    def files_creation_handler(self):
        clone_index: CloneIndex = self.detector.get__clone_index()
        for created_filename in self.creates_lst:
            self.handle_file_creation(created_filename, clone_index)

    def handle_file_creation(self, created_filename, clone_index):
        lines = CodebaseReader.get_lines_for_file(created_filename)
        created_index_entries = clone_index.calculate_index_entries_for_file(created_filename, lines)

        # detect the clones to be removed
        results = self.detector.detect_clones(created_index_entries)
        print("Clones Added")
        for group in results:
            print(group)

        # add corresponding entries to index
        clone_index.add_index_entries(created_index_entries)
