from index.CloneIndex import CloneIndex
from index.IndexEntry import IndexEntry
from CodebaseReader import CodebaseReader
from pathlib import Path
import hashlib

CHUNK_SIZE = 4

codebase = CodebaseReader(Path.home() / 'PycharmProjects/CloneDetector/data/test_project')
lines_per_files = codebase.get_lines_per_file()

clone_index = CloneIndex()

for file in lines_per_files.keys():
    print('============================================================================================================')
    print('[FILE]: ' + file)
    for i in range(0, len(lines_per_files[file]) - CHUNK_SIZE + 1):
        print("========================= BLOCK " + str(i) + " =========================")
        block_str = ''
        for j in range(i, i + CHUNK_SIZE):
            block_str += lines_per_files[file][j] + "\n"
        print(block_str)
        block_str_hash = hashlib.md5(block_str.encode("utf-8")).hexdigest()
        index_entry = IndexEntry(file, i, block_str_hash, i, i + CHUNK_SIZE)
        clone_index.add_index_entry(index_entry)

print("============================================================================================================")

clone_index.print_index()
