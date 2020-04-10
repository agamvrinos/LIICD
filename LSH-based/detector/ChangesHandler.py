import config
from typing import List
from datasketch import MinHash, MinHashLSH
from detector.CodebaseReader import CodebaseReader


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
        # TODO: Querying the LSH index could be avoided if we don't want to
        #  show which clones will be removed

        # lines for the given created file
        lines = CodebaseReader.get_lines_for_file(deleted_filename)
        # calculate min_hash based on these lines
        min_hash = self.get_minhash_for_lines(lines)

        similar_docs = self.lsh_index.query(min_hash)
        print(similar_docs)

        # TODO: calculate index entries for the similar files and run detection logic

        # remove the deleted entry from the LSH
        self.lsh_index.remove(deleted_filename)

    def files_update_handler(self):
        for updated_filename in self.updates_lst:
            self.handle_file_deletion(updated_filename)
            self.handle_file_creation(updated_filename)

    def files_creation_handler(self):
        for created_filename in self.creates_lst:
            self.handle_file_creation(created_filename)

    def handle_file_creation(self, created_filename):
        # lines for the given created file
        lines = CodebaseReader.get_lines_for_file(created_filename)
        # calculate min_hash based on these lines
        min_hash = self.get_minhash_for_lines(lines)

        similar_docs = self.lsh_index.query(min_hash)
        print(similar_docs)

        # TODO: calculate index entries for the similar files and run detection logic
        # update LSH with the new entry
        self.lsh_index.insert(created_filename, min_hash)

    def get_minhash_for_lines(self, lines):
        min_hash = MinHash(num_perm=config.PERMUTATIONS)
        for line in lines:
            min_hash.update(line.encode('utf8'))
        return min_hash
