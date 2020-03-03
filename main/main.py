from CodebaseReader import CodebaseReader
from pathlib import Path

codebase = CodebaseReader(Path.home() / 'PycharmProjects/CloneDetector/data/test_project')
lines_per_files = codebase.get_lines_per_file()

for key in lines_per_files.keys():
    print('============================================================================================================')
    print('[FILE]: ' + key)
    print('[LINES]: ' + str(lines_per_files[key]))
print("============================================================================================================")
