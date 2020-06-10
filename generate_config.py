import os
import time
import json
import argparse
import subprocess
from pathlib import Path

NUMBER_OF_COMMITS = 10
target_project_path = Path.home() / 'Desktop/Experiments/ardupilot'

parser = argparse.ArgumentParser()
parser.add_argument("-p", help="The path of the codebase for which we generate the config",
                    required=False, default=target_project_path)
parser.add_argument("-n", help="The number of commits to analyze (default 10)",
                    required=False, default=NUMBER_OF_COMMITS)

args = parser.parse_args()
if args.p:
    target_project_path = Path(args.p)
if args.n:
    NUMBER_OF_COMMITS = args.n

JSON_data = {'commits': []}

result = subprocess.run(['git', '-C', str(target_project_path),
                         'log', '-' + str(NUMBER_OF_COMMITS), '--no-merges', '--pretty=format:"%h"'],
                        stdout=subprocess.PIPE)

commits = result.stdout.decode('utf-8')
commits = commits.replace('"', '')
commits = commits.split('\n')

print(commits)

# reverse list of commits to iterate from older to the newer ones
commits_rev = [ele for ele in reversed(commits)]

for commit in commits_rev:
    JSON_changes = []

    print('=======================================')
    print('CHECKING OUT TO: ' + commit)
    print('=======================================')

    # checkout to the current commit
    subprocess.run(['git', '-C', str(target_project_path),
                    'checkout', commit], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # get raw commit log
    changes = subprocess.run(['git', '-C', str(target_project_path),
                              'log', '-1', '--name-status', '--diff-filter=AMD', '--format='], stdout=subprocess.PIPE)

    changes = changes.stdout.decode('utf-8')
    changes = changes.split("\n")
    for change in changes:
        if not change:
            continue

        print(change)
        change_type, filename = change.split("\t")

        JSON_changes.append({
            'type': change_type,
            'filename': filename
        })

    JSON_data['commits'].append({
        'id': commit,
        'changes': JSON_changes
    })

    time.sleep(4)

    print('=======================================')
    print('CHECKING OUT BACK TO HEAD')
    print('=======================================')

    # checkout back to HEAD
    subprocess.run(['git', '-C', str(target_project_path),
                    'checkout', '-'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    time.sleep(4)


# create config files directory
directory_name = 'configurations'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

updates_filename = directory_name / Path(target_project_path.stem + '_updates.json')

with open(updates_filename, 'w') as outfile:
    json.dump(JSON_data, outfile, indent=4)
