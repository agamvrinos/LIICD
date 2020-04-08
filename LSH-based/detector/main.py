import json
from pathlib import Path
from datasketch import MinHash, MinHashLSH
from timeit import default_timer as timer
from detector.CodebaseReader import CodebaseReader

project_path = input("Provide the project path: ")
if not project_path:
    project_path = Path.home() / 'Desktop/data/test_project'
    print("Empty path provided. Setting default project path \"" + str(project_path) + "\"")

# start the timer
# start = timer()

codebase = CodebaseReader(project_path)
lines_per_files = codebase.get_lines_per_file()

# Create LSH index
lsh = MinHashLSH(threshold=0.2, num_perm=250)

for file in lines_per_files:
    min_hash = MinHash(num_perm=250)
    for line in lines_per_files[file]:
        min_hash.update(line.encode('utf8'))
    lsh.insert(file, min_hash)

updates_path = input("Provide the updates file path: ")
if not updates_path:
    updates_path = Path.home() / 'Desktop/data/updates.json'
    print("Empty path provided. Setting default updates path \"" + str(updates_path) + "\"")

while True:
    creates_lst = []
    updates_lst = []
    deletes_lst = []

    try:
        input("Waiting for codebase changes...")

        with open(updates_path) as f:
            changes = json.load(f)
            for change in changes:
                if change['type'] == 'create':
                    creates_lst.append(change['path'])
                elif change['type'] == 'update':
                    updates_lst.append(change['path'])
                elif change['type'] == 'delete':
                    deletes_lst.append(change['path'])
    except IOError:
        print("File \"" + str(updates_path) + "\" not found.")

# lsh.insert("m2", m2)
# # lsh.insert("m3", m1)
# result = lsh.query(m1)
# print("Approximate neighbours with Jaccard similarity > 0.5", result)
