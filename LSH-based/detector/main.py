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

for file in lines_per_files:
    print(file)
    for line in lines_per_files[file]:
        print(line)
