import json
import argparse
from pathlib import Path
from detector.clone.CloneDetector import CloneDetector
from detector.index.CloneIndex import CloneIndex
from detector.CodebaseReader import CodebaseReader
from detector.ChangesHandler import ChangesHandler
from timeit import default_timer as timer

# from memory_profiler import profile
#
#
# @profile
def run(codebase_path, updates_file_path):
    # start the timer
    start = timer()

    codebase = CodebaseReader(codebase_path)
    lines_per_files = codebase.get_lines_per_file()

    clone_index = CloneIndex()

    for file in lines_per_files.keys():
        index_entries = clone_index.calculate_index_entries_for_file(file, lines_per_files[file])
        clone_index.add_index_entries(index_entries)

    end = timer()

    print("============================================================")
    print("Total LOCs: ", str(codebase.get__initial_codebase_lines()))
    print("Index creation time: " + str(round(end-start, 5)) + " seconds")
    print("============================================================")

    detector = CloneDetector(clone_index)

    while True:
        creates_lst = []
        updates_lst = []
        deletes_lst = []

        try:
            key = input("Waiting for codebase changes...")
            if key == "quit":
                quit()

            with open(updates_file_path) as f:
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
            print("File \"" + str(updates_file_path) + "\" not found.")


codebase_path = Path.home() / 'Desktop/data/homebrew-core'
updates_file_path = Path.home() / 'Desktop/data/updates.json'

parser = argparse.ArgumentParser(description="Runs the LSH-based clone detector")
parser.add_argument("-p", "--path", help="The path of the codebase to be analyzed",
                    required=False, default=codebase_path)
parser.add_argument("-u", "--upath", help="The path of the file that indicates the updates",
                    required=False, default=updates_file_path)

argument = parser.parse_args()
status = False

if argument.path:
    codebase_path = argument.path
    status = True
if argument.upath:
    updates_file_path = argument.upath
    status = True
if not status:
    print("Maybe you want to use -p or -u as arguments ?")


run(codebase_path, updates_file_path)
