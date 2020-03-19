from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex
from detector.CodebaseReader import CodebaseReader
from pathlib import Path

CHUNK_SIZE = 4
project_path = Path.home() / 'PycharmProjects/CloneDetector/data/test_project'

codebase = CodebaseReader(project_path)
lines_per_files = codebase.get_lines_per_file()

clone_index = CloneIndex()

for file in lines_per_files.keys():
    index_entries = clone_index.calculate_index_entries_for_file(file, lines_per_files[file], CHUNK_SIZE)
    clone_index.add_index_entries(index_entries)

clone_index.print_index()

# A hardcoded simulation of a newly added file
new_file_path = str(Path.home() / 'PycharmProjects/CloneDetector/data/New.java')
new_file_lines = codebase.get_lines_for_file(new_file_path)
new_file_index_entries = clone_index.calculate_index_entries_for_file(new_file_path, new_file_lines, CHUNK_SIZE)

clone_detector = CloneDetector(clone_index)
results = clone_detector.detect_clones(new_file_index_entries)
for result in results:
    for part in result.get__parts():
        split_arr = part.filename.split("\\")
        part.filename = split_arr[len(split_arr) - 1]
    print(result)
