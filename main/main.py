from index.CloneIndex import CloneIndex
from index.IndexEntry import IndexEntry
from CodebaseReader import CodebaseReader
from pathlib import Path

codebase = CodebaseReader(Path.home() / 'PycharmProjects/CloneDetector/data/test_project')
lines_per_files = codebase.get_lines_per_file()

for key in lines_per_files.keys():
    print('============================================================================================================')
    print('[FILE]: ' + key)
    print('[LINES]: ' + str(lines_per_files[key]))
print("============================================================================================================")

index_entry = IndexEntry("Test.java", 0, "43453", 0, 4)
index_entry_2 = IndexEntry("Test.java", 1, "43455", 1, 5)

clone_index = CloneIndex()
clone_index.add_index_entry(index_entry)
clone_index.add_index_entry(index_entry_2)
clone_index.print_index()