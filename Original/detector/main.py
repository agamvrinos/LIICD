import json
from pathlib import Path
from utils.utils import get_size
from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex
from detector.CodebaseReader import CodebaseReader
from detector.ChangesHandler import ChangesHandler
from timeit import default_timer as timer

project_path = input("Provide the project path: ")
if not project_path:
    project_path = Path.home() / 'Desktop/data/test_project'
    print("Empty path provided. Setting default project path \"" + str(project_path) + "\"")

# start the timer
start = timer()

codebase = CodebaseReader(project_path)
lines_per_files = codebase.get_lines_per_file()

clone_index = CloneIndex()

for file in lines_per_files.keys():
    index_entries = clone_index.calculate_index_entries_for_file(file, lines_per_files[file])
    clone_index.add_index_entries(index_entries)

end = timer()

print("============================================================")
print("Total LOCs: ", str(codebase.get__initial_codebase_lines()))
print("Index creation time: " + str(round(end-start, 5)) + " seconds")
print("Approx. Index size: " + str(
    round((get_size(clone_index.index_entries_by_file) + get_size(clone_index.index_entries_by_hash)) / pow(1024, 2), 5)) + " MB")
print("============================================================")

detector = CloneDetector(clone_index)

updates_path = input("Provide the updates file path: ")
if not updates_path:
    updates_path = Path.home() / 'Desktop/data/updates.json'
    print("Empty path provided. Setting default updates path \"" + str(updates_path) + "\"")

while True:
    creates_lst = []
    updates_lst = []
    deletes_lst = []

    try:
        key = input("Waiting for codebase changes...")
        if key == "quit":
            quit()

        with open(updates_path) as f:
            changes = json.load(f)
            for change in changes:
                if change['type'] == 'create':
                    creates_lst.append(change['path'])
                elif change['type'] == 'update':
                    updates_lst.append(change['path'])
                elif change['type'] == 'delete':
                    deletes_lst.append(change['path'])

        changes_handler = ChangesHandler(detector, deletes_lst, updates_lst, creates_lst)

        # start incremental step timer
        start = timer()
        # handle commit changes
        changes_handler.handle_changes()
        # end incremental step timer
        end = timer()
        print("Detection/Index update time: " + str(round(end - start, 5)) + " seconds")

        f.close()
    except IOError:
        print("File \"" + str(updates_path) + "\" not found.")
