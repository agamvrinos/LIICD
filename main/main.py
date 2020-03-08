from index.CloneDetector import CloneDetector
from index.CloneIndex import CloneIndex
from index.IndexEntry import IndexEntry
from CodebaseReader import CodebaseReader
from pathlib import Path
import hashlib

CHUNK_SIZE = 4


def calculate_index_entries_for_file(file, lines):
    print('============================================================================================================')
    print('[FILE]: ' + file)
    index_entries = []
    for i in range(0, len(lines) - CHUNK_SIZE + 1):
        print("========================= BLOCK " + str(i) + " =========================")
        block_str = ''
        for j in range(i, i + CHUNK_SIZE):
            block_str += lines[j] + "\n"
        print(block_str)
        block_str_hash = hashlib.md5(block_str.encode("utf-8")).hexdigest()
        index_entry = IndexEntry(file, i, block_str_hash, i, i + CHUNK_SIZE)
        index_entries.append(index_entry)
    return index_entries


codebase = CodebaseReader(Path.home() / 'PycharmProjects/CloneDetector/data/test_project')
lines_per_files = codebase.get_lines_per_file()

clone_index = CloneIndex()

for file in lines_per_files.keys():
    index_entries = calculate_index_entries_for_file(file, lines_per_files[file])
    for entry in index_entries:
        clone_index.add_index_entry(entry)
print("============================================================================================================")

clone_index.print_index()

# A hardcoded simulation of a newly added file
new_file_path = str(Path.home() / 'PycharmProjects/CloneDetector/data/New.java')
new_file_lines = codebase.get_lines_for_file(new_file_path)
new_file_index_entries = calculate_index_entries_for_file(new_file_path, new_file_lines)

clone_detector = CloneDetector(clone_index)
# clone_detector.detect_clones(new_file_index_entries)
