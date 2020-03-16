from typing import Dict, List
from detector.index.IndexEntry import IndexEntry


class CloneIndex:

    index_entries_by_file: Dict[str, List[IndexEntry]] = {}
    index_entries_by_hash: Dict[str, List[IndexEntry]] = {}

    def get__index_entries_by_file(self):
        return self.index_entries_by_file

    def get__index_entries_by_hash(self):
        return self.index_entries_by_hash

    def add_index_entry(self, index_entry):
        self.index_entries_by_file.setdefault(index_entry.get__file_name(), []).append(index_entry)
        self.index_entries_by_hash.setdefault(index_entry.get__sequence_hash(), []).append(index_entry)

    def add_index_entries(self, index_entries):
        for index_entry in index_entries:
            self.add_index_entry(index_entry)

    def print_index(self):
        for file in self.index_entries_by_file.keys():
            print("[INDEX FOR FILE]: " + file)
            for idx in range(len(self.index_entries_by_file[file])):
                print("[ENTRY " + str(idx) + "]", end=" ")
                print(self.index_entries_by_file[file][idx])
        for hash in self.index_entries_by_hash.keys():
            print("[INDEX FOR HASH]: " + hash)
            for idx in range(len(self.index_entries_by_hash[hash])):
                print("[ENTRY " + str(idx) + "]", end=" ")
                print(self.index_entries_by_hash[hash][idx])
