import time
import json
import subprocess

NUMBER_OF_COMMITS = 2

JSON_data = {'commits': []}

result = subprocess.run(['git', 'log', '-' + str(NUMBER_OF_COMMITS), '--no-merges', '--pretty=format:"%h"'], stdout=subprocess.PIPE)
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
    subprocess.run(['git', 'checkout', commit], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # get raw commit log
    changes = subprocess.run(['git', 'log', '-1', '--name-status', '--diff-filter=AMD', '--format='], stdout=subprocess.PIPE)
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

    time.sleep(2)

    print('=======================================')
    print('CHECKING OUT BACK TO HEAD')
    print('=======================================')

    # checkout back to HEAD
    subprocess.run(['git', 'checkout', '-'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    time.sleep(2)

with open('data.json', 'w') as outfile:
    json.dump(JSON_data, outfile, indent=4)
