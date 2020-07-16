from detector import config
from typing import List
from datasketch import MinHash, MinHashLSH
from detector.index.CloneIndex import CloneIndex
from detector.CodebaseReader import CodebaseReader
from detector.clone.CloneDetector import CloneDetector


class ChangesHandler:

    def __init__(self, lsh_index, codebase_reader, deletes_lst, updates_lst, creates_lst, renames_lst):
        self.lsh_index: MinHashLSH = lsh_index
        self.codebase_reader = codebase_reader
        self.deletes_lst: List = deletes_lst
        self.updates_lst: List = updates_lst
        self.creates_lst: List = creates_lst
        self.renames_lst: List = renames_lst

    def handle_changes(self):
        if len(self.deletes_lst) != 0:
            self.files_deletion_handler()
        if len(self.renames_lst) != 0:
            self.files_rename_handler()
        if len(self.updates_lst) != 0:
            self.files_update_handler()
        if len(self.creates_lst) != 0:
            self.files_creation_handler()

    def files_deletion_handler(self):
        for deleted_filename in self.deletes_lst:
            self.handle_file_deletion(deleted_filename)

    def handle_file_deletion(self, deleted_filename):
        # TODO: Querying the LSH index & constructing the index could be
        #  avoided if we don't want to show which clones will be removed

        # lines for the given deleted file
        lines = self.codebase_reader.get_lines_per_file()[deleted_filename]
        # calculate min_hash based on these lines
        min_hash = self.get_minhash_for_lines(lines)
        # query LSH index to find out which files are similar to the deleted one
        similar_docs = self.lsh_index.query(min_hash)
        # print(similar_docs)

        results = self.detect_clones_for_similar_files(deleted_filename, lines, similar_docs)
        print("Clones Removed")
        for group in results:
            if len(set(group.get__parts())) > 1:
                print(group)

        # remove the deleted entry from the LSH
        self.lsh_index.remove(deleted_filename)

    def files_rename_handler(self):
        for renames_tuple in self.renames_lst:
            self.handle_file_deletion(renames_tuple[0])
            self.handle_file_creation(renames_tuple[1])

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
        # update codebase reader instance with the new lines
        self.codebase_reader.lines_per_file[created_filename] = lines
        # calculate min_hash based on these lines
        min_hash = self.get_minhash_for_lines(lines)
        # query LSH index to find out which files are similar to the created one
        similar_docs = self.lsh_index.query(min_hash)
        # print(similar_docs)

        results = self.detect_clones_for_similar_files(created_filename, lines, similar_docs)
        print("Clones Added")
        for group in results:
            if len(set(group.get__parts())) > 1:
                print(group)

        # update LSH with the new entry
        self.lsh_index.insert(created_filename, min_hash)

    def detect_clones_for_similar_files(self, filename, lines, similar_docs):
        mini_clone_index = CloneIndex()
        mini_clone_index.index_entries_by_hash.clear()
        mini_clone_index.index_entries_by_file.clear()

        for similar_doc in similar_docs:
            similar_doc_lines = self.codebase_reader.get_lines_per_file()[similar_doc]
            similar_doc_index_entries = CloneIndex.calculate_index_entries_for_file(similar_doc, similar_doc_lines)
            mini_clone_index.add_index_entries(similar_doc_index_entries)

        # Init clone detector using the mini index
        detector = CloneDetector(mini_clone_index)
        current_file_index_entries = CloneIndex.calculate_index_entries_for_file(filename, lines)

        results = detector.detect_clones(current_file_index_entries)
        return results

    def get_minhash_for_lines(self, lines):
        min_hash = MinHash(num_perm=config.PERMUTATIONS)
        for line in lines:
            min_hash.update(line.encode('utf8'))
        return min_hash
