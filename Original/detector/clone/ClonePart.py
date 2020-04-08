class ClonePart:

    def __init__(self, filename, unit_start, start_line, end_line):
        self.filename = filename
        self.unit_start = unit_start
        self.start_line = start_line
        self.end_line = end_line

    def __eq__(self, other):
        if isinstance(other, ClonePart):
            return self.filename == other.filename and \
                   self.unit_start == other.unit_start and \
                   self.start_line == other.start_line and \
                   self.end_line == other.end_line
        return False

    def __str__(self):
        return "(" + self.filename + "|" + str(self.unit_start) + "|" + \
               str(self.start_line) + "-" + str(self.end_line) + ")"

    def get__filename(self):
        return self.filename

    def get__unit_start(self):
        return self.unit_start

    def get__start_line(self):
        return self.start_line

    def get__end_line(self):
        return self.end_line
