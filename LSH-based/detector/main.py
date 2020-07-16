import json
import argparse
import subprocess
import traceback
from detector import config
from pathlib import Path
from datasketch import MinHash, MinHashLSH
from detector.ChangesHandler import ChangesHandler
from detector.CodebaseReader import CodebaseReader
from timeit import default_timer as timer

# from memory_profiler import profile


# @profile
def run(codebase_path, updates_file_path, commits):

    print("Creating Clone Index from HEAD~" + str(commits + 1))

    result = subprocess.run(['git', '-C', str(codebase_path),
                             'log', '-' + str(commits + 1), '--no-merges', '--pretty=format:"%h"'],
                            stdout=subprocess.PIPE)

    result_commits = result.stdout.decode('utf-8')
    result_commits = result_commits.replace('"', '')
    result_commits = result_commits.split('\n')

    # checkout to the current commit
    subprocess.run(['git', '-C', str(codebase_path), 'checkout', result_commits[len(result_commits) - 1]],
                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # start the timer
    index_cr_start = timer()

    codebase = CodebaseReader(codebase_path)
    lines_per_files = codebase.get_lines_per_file()

    # Create LSH index
    lsh_index = MinHashLSH(threshold=config.THRESHOLD, num_perm=config.PERMUTATIONS)

    for file in lines_per_files:
        min_hash = MinHash(num_perm=config.PERMUTATIONS)
        for line in lines_per_files[file]:
            min_hash.update(line.encode('utf8'))
        lsh_index.insert(file, min_hash)

    index_cr_end = timer()
    index_cr_diff = round(index_cr_end - index_cr_start, 5)

    incremental_step_time = 0
    commits_processed = 0  # we use this instead of len(data['commits']) bcs there might me commits that only affect
                           # excluded (e.g. test) files and in that case the specific commit does not get processed

    try:
        with open(updates_file_path) as f:
            data = json.load(f)
            commits = data['commits']

            for commit in commits:
                creates_lst = []
                updates_lst = []
                deletes_lst = []
                renames_lst = []

                print('========> Running Analysis for codebase @commit: ', commit['id'], "<========")

                # checkout to the current commit
                subprocess.run(['git', '-C', str(codebase_path), 'checkout', commit['id']],
                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

                is_processed = False

                for change in commit['changes']:
                    change_type = change['type']

                    if change_type in ['A', 'M', 'D']:
                        affected_filename = change['filename']
                        file_path = Path(affected_filename)

                        # skip directories not read when creating the initial index & skip invalid files
                        if is_in_exlcuded_dir(file_path) or is_in_excluded_format(file_path):
                            continue

                        is_processed = True  # if I get here then there is at least 1 change in that commit that is processed

                        file_path = codebase_path / file_path

                        print('-> Parsing change [', change_type, '] for file [', file_path, ']')

                        if change_type == 'A':
                            creates_lst.append(str(file_path))
                        elif change_type == 'M':
                            updates_lst.append(str(file_path))
                        elif change_type == 'D':
                            deletes_lst.append(str(file_path))
                    else:
                        affected_filenames = change['filename']
                        from_filename = Path(affected_filenames[0])
                        to_filename = Path(affected_filenames[1])

                        # skip directories not read when creating the initial index & skip invalid files
                        if is_in_exlcuded_dir(from_filename) or is_in_excluded_format(from_filename) or \
                                is_in_exlcuded_dir(to_filename) or is_in_excluded_format(to_filename):
                            continue

                        is_processed = True  # if I get here then there is at least 1 change in that commit that is processed

                        from_filename = codebase_path / from_filename
                        to_filename = codebase_path / to_filename

                        print('-> Parsing change [', change_type, '] for renamed/moved file [', from_filename, ']',
                              'to [', to_filename, ']')

                        renames_lst.append((str(from_filename), str(to_filename)))

                if is_processed:
                    changes_handler = ChangesHandler(lsh_index, codebase,
                                                     deletes_lst, updates_lst, creates_lst, renames_lst)
                    # start incremental step timer
                    start = timer()
                    # handle commit changes
                    changes_handler.handle_changes()
                    # end incremental step timer
                    end = timer()
                    time_diff = round(end - start, 5)
                    print("Detection/Index update time: " + str(time_diff) + " seconds")

                    commits_processed += 1
                    incremental_step_time += time_diff
                else:
                    print("Commit " + commit['id'] + " was skipped because all files were excluded")

                # checkout back to HEAD
                subprocess.run(['git', '-C', str(codebase_path), 'checkout', '-'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            print("============================================================")
            print("Total LOCs: ", codebase.get__initial_codebase_lines())
            print("Total Index creation time: ", index_cr_diff, " seconds")
            print("Total commits: ", len(commits))
            print("Total commits processed: ", commits_processed)
            if commits_processed > 0:
                print("Average Incremental Step Time: ", round(incremental_step_time / float(commits_processed), 5),
                      " seconds")
            else:
                print("0 commits out of ", len(commits), " were processed. Something went terribly wrong!")
            print("============================================================")

        f.close()
    except IOError:
        traceback.print_exc()
        print("File \"" + str(updates_file_path) + "\" not found.")


def is_in_exlcuded_dir(file_path):
    found_excluded = False
    for path_part in file_path.parts:
        if path_part in config.SKIP_DIRS or path_part[0] == '.':
            found_excluded = True
            break
    return found_excluded


def is_in_excluded_format(file_path):
    return (file_path.suffix in config.SKIP_FILES) or file_path.suffix is ''


codebase_path = Path.home() / 'Desktop/Experiments/tensorflow'
updates_file_path = Path.home() / 'PycharmProjects/CloneDetector/configurations' / Path(codebase_path.stem + '_updates.json')

parser = argparse.ArgumentParser(description="Runs the LSH-based clone detector")
parser.add_argument("-p", "--path", help="The path of the codebase to be analyzed",
                    required=False, default=codebase_path)
parser.add_argument("-u", "--upath", help="The path of the file that indicates the updates",
                    required=False, default=updates_file_path)
parser.add_argument("-c", "--commits", help="The path of the file that indicates the updates",
                    required=False, default=config.COMMITS)

argument = parser.parse_args()
status = False

if argument.path:
    codebase_path = argument.path
    status = True
if argument.upath:
    updates_file_path = argument.upath
    status = True
if argument.commits:
    commits = int(argument.commits)
    status = True
if not status:
    print("Maybe you want to use -p or -u as arguments ?")


run(codebase_path, updates_file_path, commits)
