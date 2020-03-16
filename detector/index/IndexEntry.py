class IndexEntry:

    def __init__(self, file_name, statement_index, sequence_hash, start_line, end_line):
        self.file_name = file_name
        self.statement_index = statement_index
        self.sequence_hash = sequence_hash
        self.start_line = start_line
        self.end_line = end_line

    def __str__(self):
        return self.file_name + " [" + str(self.statement_index) + " | " + \
               str(self.start_line) + "-" + str(self.end_line) + "], " + self.sequence_hash

    def get__file_name(self):
        return self.file_name

    def get__statement_index(self):
        return self.statement_index

    def get__sequence_hash(self):
        return self.sequence_hash

    def get__start_line(self):
        return self.start_line

    def get__end_line(self):
        return self.end_line
