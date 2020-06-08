import json
import argparse
import subprocess
import detector.config as config
from pathlib import Path
from datasketch import MinHash, MinHashLSH
from ChangesHandler import ChangesHandler
from CodebaseReader import CodebaseReader
from timeit import default_timer as timer

# from memory_profiler import profile


# @profile
def run(codebase_path, updates_file_path):

    print("Creating Clone Index from HEAD~" + str(config.COMMITS + 1))
    # checkout to the commit prior to the one you want to start measuring from
    subprocess.run(['git', '-C', str(codebase_path), 'checkout', 'HEAD~' + str(config.COMMITS + 1)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

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
                    affected_filename = change['filename']

                    file_path = Path(affected_filename)

                    # skip directories not read when creating the initial index
                    for path_part in file_path.parts:
                        if path_part in config.SKIP_DIRS:
                            continue

                    # skip files in binary format
                    if file_path.suffix in config.SKIP_FILES:
                        continue

                    file_path = codebase_path / file_path

                    print('-> Parsing change [', change_type, '] for file [', file_path, ']')

                    if change_type == 'A':
                        creates_lst.append(str(file_path))
                    elif change_type == 'M':
                        updates_lst.append(str(file_path))
                    elif change_type == 'D':
                        deletes_lst.append(str(file_path))

                changes_handler = ChangesHandler(lsh_index, deletes_lst, updates_lst, creates_lst)
                # start incremental step timer
                start = timer()
                # handle commit changes
                changes_handler.handle_changes()
                # end incremental step timer
                end = timer()
                print("Detection/Index update time: " + str(round(end - start, 5)) + " seconds")
                print('=======================================================')

                # checkout back to HEAD
                subprocess.run(['git', '-C', str(codebase_path), 'checkout', '-'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        f.close()
    except IOError:
        print("File \"" + str(updates_file_path) + "\" not found.")


codebase_path = Path.home() / 'Desktop/data/tensorflow'
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
