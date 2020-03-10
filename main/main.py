from clone.CloneDetector import CloneDetector
from index.CloneIndex import CloneIndex
from index.IndexEntry import IndexEntry
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


def test_index():
    test_clone_index = CloneIndex()
    test_clone_index.add_index_entry(IndexEntry("A.java", 0, "398ae43bfd41e541ea738a48aef3669e", 0, 4))
    test_clone_index.add_index_entry(IndexEntry("A.java", 1, "a11ccfbc32959dbf0e316ac7d1e46d95", 1, 5))
    test_clone_index.add_index_entry(IndexEntry("A.java", 2, "10ead5822589a0b68bbbfec6a1c520af", 2, 6))
    test_clone_index.add_index_entry(IndexEntry("C.java", 0, "a11ccfbc32959dbf0e316ac7d1e46d95", 0, 4))

    new_file_index_entry_1 = IndexEntry("B.java", 0, "398ae43bfd41e541ea738a48aef3669e", 0, 4)
    new_file_index_entry_2 = IndexEntry("B.java", 1, "a11ccfbc32959dbf0e316ac7d1e46d95", 1, 5)
    new_file_index_entry_3 = IndexEntry("B.java", 2, "aaaabbbb37cc8122c89d98a51f88084b", 2, 6)

    detector = CloneDetector(test_clone_index)
    results = detector.detect_clones([new_file_index_entry_1, new_file_index_entry_2, new_file_index_entry_3])

    for group in results:
        print("== NEW GROUP ==")
        print(group)

# codebase = CodebaseReader(Path.home() / 'PycharmProjects/CloneDetector/data/test_project')
# lines_per_files = codebase.get_lines_per_file()
#
# clone_index = CloneIndex()
#
# for file in lines_per_files.keys():
#     index_entries = calculate_index_entries_for_file(file, lines_per_files[file])
#     for entry in index_entries:
#         clone_index.add_index_entry(entry)
# print("============================================================================================================")
#
# clone_index.print_index()
#
# # A hardcoded simulation of a newly added file
# new_file_path = str(Path.home() / 'PycharmProjects/CloneDetector/data/New.java')
# new_file_lines = codebase.get_lines_for_file(new_file_path)
# new_file_index_entries = calculate_index_entries_for_file(new_file_path, new_file_lines)
#
# clone_detector = CloneDetector(clone_index)
# clone_detector.detect_clones(new_file_index_entries)

test_index()
