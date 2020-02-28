import os


class CodebaseReader:

    files = []

    def __init__(self, path):
        self.path = str(path)
        for root, directories, filenames in os.walk(self.path):
            for filename in filenames:
                self.files.append(os.path.join(root, filename))

    def get__path(self):
        return self.path

    def get_files(self):
        return self.files
