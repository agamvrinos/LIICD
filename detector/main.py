from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex
from detector.CodebaseReader import CodebaseReader
from detector.watcher.FileWatcher import FileWatcher
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


watch_directory = str(Path.home() / 'Desktop/data')
watcher = FileWatcher(watch_directory)
watcher.run()
