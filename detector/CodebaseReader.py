import os


class CodebaseReader:
    """
    Recursively reads all the files under the given path and stores
    the files themselves as well as the lines corresponding to each file.

    Args:
        files (str[]): The paths of the files under the root directory
        lines_per_file (dict): A dictionary with files pointing to the
        respective lines per file.

    Attributes:
        path (POSIX Path): The path pointing to the root of the codebase
        to be read.
    """

    files = []
    lines_per_file = {}

    def __init__(self, path):
        self.path = str(path)
        for root, directories, filenames in os.walk(self.path):
            for filename in filenames:
                join = os.path.join(root, filename)
                self.files.append(join)
                lines = CodebaseReader.get_lines_for_file(join)
                self.lines_per_file[join] = lines

    def get__path(self):
        return self.path

    def get_files(self):
        return self.files

    def get_lines_per_file(self):
        return self.lines_per_file

    @staticmethod
    def get_lines_for_file(path):
        with open(path, encoding='utf-8') as fp:
            lines = []
            for line in fp:
                line = line.strip()
                line = " ".join(line.split())
                if line:
                    lines.append(line)
        fp.close()
        return lines
