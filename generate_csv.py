"""
Generates the configuration file for the script that automates the
commit simulation for the SAT experiments.
"""

import csv
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


result = subprocess.run(['git', '-C', str(target_project_path),
                         'log', '-' + str(NUMBER_OF_COMMITS), '--no-merges', '--pretty=format:"%H"'],
                        stdout=subprocess.PIPE)

commits = result.stdout.decode('utf-8')
commits = commits.replace('"', '')
commits = commits.split('\n')
print(commits)

commits_rev = [ele for ele in reversed(commits)]

config_file = 'sat_input_' + target_project_path.stem + '.csv'
with open(config_file, mode='w', newline='') as config_file:
    writer = csv.writer(config_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['issueId', 'projectName', 'sha'])

    i = 0
    for commit in commits_rev:
        writer.writerow([i, target_project_path.stem, commit])
        i += 1
