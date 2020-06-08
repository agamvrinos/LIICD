import json
import config
import argparse
from pathlib import Path
from datasketch import MinHash, MinHashLSH
from timeit import default_timer as timer
from ChangesHandler import ChangesHandler
from CodebaseReader import CodebaseReader
# from memory_profiler import profile


# @profile
def run(codebase_path, updates_file_path):
    # start the timer
    start = timer()

    codebase = CodebaseReader(codebase_path)
    lines_per_files = codebase.get_lines_per_file()

    # Create LSH index
    lsh_index = MinHashLSH(threshold=config.THRESHOLD, num_perm=config.PERMUTATIONS)

    for file in lines_per_files:
        min_hash = MinHash(num_perm=config.PERMUTATIONS)
        for line in lines_per_files[file]:
            min_hash.update(line.encode('utf8'))
        lsh_index.insert(file, min_hash)

    end = timer()

    print("============================================================")
    print("Total LOCs: ", str(codebase.get__initial_codebase_lines()))
    print("Index creation time: " + str(round(end-start, 5)) + " seconds")
    print("============================================================")

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

            changes_handler = ChangesHandler(lsh_index, deletes_lst, updates_lst, creates_lst)
            changes_handler.handle_changes()
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
