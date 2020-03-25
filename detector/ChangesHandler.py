from typing import List
from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex


class ChangesHandler:

    def __init__(self, detector, deletes_lst, updates_lst, creates_lst):
        self.detector: CloneDetector = detector
        self.deletes_lst: List = deletes_lst
        self.updates_lst: List = updates_lst
        self.creates_lst: List = creates_lst

    def handle_changes(self):
        self.files_deletion_handler()
        self.files_update_handler()
        self.files_creation_handler()

    def files_deletion_handler(self):
        for deleted_filename in self.deletes_lst:
            clone_index: CloneIndex = self.detector.get__clone_index()
            index_entries_by_file = clone_index.get__index_entries_by_file()
            deleted_index_entries = index_entries_by_file[deleted_filename]

            # detect the clones to be removed
            results = self.detector.detect_clones(deleted_index_entries)
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
        return

    def files_creation_handler(self):
        return
