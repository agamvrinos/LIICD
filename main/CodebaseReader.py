import os


class CodebaseReader:

    files = []
    lines_per_file = {}

    def __init__(self, path):
        self.path = str(path)
        for root, directories, filenames in os.walk(self.path):
            for filename in filenames:
                join = os.path.join(root, filename)
                self.files.append(join)
                lines = self.get_lines_for_file(join)
                self.lines_per_file[join] = lines

    def get__path(self):
        return self.path

    def get_files(self):
        return self.files

    def get_lines_per_file(self):
        return self.lines_per_file

    def get_lines_for_file(self, path):
        with open(path) as fp:
            lines = []
            for line in fp:
                line = line.strip()
                if line:
                    lines.append(line)
        return lines
