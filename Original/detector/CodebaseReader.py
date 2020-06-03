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
    total_lines = 0
    SKIP_DIRS = [
        'node_modules', 'assets', 'build', 'classes', 'gradle', 'licenses', 'icu', 'dcn21',
        'fixtures', 'docs', 'test', 'tests', 'examples'
    ]
    SKIP_FILES = [
        '.tar', '.ico', '.png', '.jpg', '.jpeg', '.txt', '.md', '.bat', '.sh', '.jks',
        '.prpt', '.pyc', '.bmp', '.ini', '.db', '.gif', '.plist', '.ver', '.ogv',
        '.swf', '.xpi', '.icns', '.ogg', '.eot', '.ttf', '.woff', '.pb', '.data-00000-of-00001',
        '.index', '.golden', '.pbtxt.gz', '.wav', '.bin', '.mdb', '.meta', '.bytes', '.lite', '.h5',
        '.data-00000-of-00002', '.data-00001-of-00002', '.mp4', '.map', '.woff2', '.pdf', '.exe',
        '.scpt', '.elf', '.skb', '.skp', '.rgb', '.a', 'zip', '.dtbo', '.3ds', '.mat', '.fig', '.pfx',
        '.dll', '.cs'
    ]

    def __init__(self, path):
        self.path = str(path)
        for root, directories, filenames in os.walk(self.path):
            filenames2 = []
            for f in filenames:
                split_path = f.split(os.sep)
                is_without_extension = len(split_path[len(split_path) - 1].split(".")) == 1
                if not (f[0] == '.' or f.endswith(tuple(self.SKIP_FILES)) or is_without_extension):
                    filenames2.append(f)
                # else:
                #     print("Skipping file \"" + f + "\"")

            filenames = filenames2

            directories[:] = [d for d in directories if not (d[0] == '.' or d in self.SKIP_DIRS)]

            for filename in filenames:
                join = os.path.join(root, filename)
                lines = CodebaseReader.get_lines_for_file(join)
                if lines is None:
                    continue
                self.files.append(join)
                self.lines_per_file[join] = lines
                self.total_lines = self.total_lines + len(lines)

    def get__path(self):
        return self.path

    def get_files(self):
        return self.files

    def get_lines_per_file(self):
        return self.lines_per_file

    def get__initial_codebase_lines(self):
        return self.total_lines

    @staticmethod
    def get_lines_for_file(path):
        try:
            with open(path, encoding='utf-8') as fp:
                lines = []
                for line in fp:
                    line = line.strip()
                    line = " ".join(line.split())
                    if line:
                        lines.append(line)
            fp.close()
            return lines
        except UnicodeDecodeError:
            print("Skipping binary file: ", path)
            return None
