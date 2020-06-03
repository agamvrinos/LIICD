import json
import argparse
import subprocess
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

    try:
        with open(updates_file_path) as f:
            data = json.load(f)

            for commit in data['commits']:
                creates_lst = []
                updates_lst = []
                deletes_lst = []

                print('============================================================')
                print('Running Analysis for codebase @commit: ', commit['id'])

                # checkout to the current commit
                subprocess.run(['git', '-C', str(codebase_path),
                                'checkout', commit['id']], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                for change in commit['changes']:
                    change_type = change['type']

                    file_path = Path(change['filename'])
                    file_path = codebase_path / file_path

                    print('-> Parsing change [', change_type, '] for file [', file_path, ']')

                    if change_type == 'A':
                        creates_lst.append(file_path)
                    elif change_type == 'M':
                        updates_lst.append(file_path)
                    elif change_type == 'D':
                        deletes_lst.append(file_path)

                changes_handler = ChangesHandler(detector, deletes_lst, updates_lst, creates_lst)
                # start incremental step timer
                start = timer()
                # handle commit changes
                changes_handler.handle_changes()
                # end incremental step timer
                end = timer()
                print("Detection/Index update time: " + str(round(end - start, 5)) + " seconds")
                print('=======================================================')

                # checkout back to HEAD
                subprocess.run(['git', '-C', str(codebase_path),
                                'checkout', '-'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        f.close()
    except IOError:
        print("File \"" + str(updates_file_path) + "\" not found.")


codebase_path = Path.home() / 'Desktop/Experiments/tensorflow'
updates_file_path = Path.home() / 'PycharmProjects/CloneDetector/configurations' / Path(codebase_path.stem + '_updates.json')

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
