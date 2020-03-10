from typing import List
from clone.ClonePart import ClonePart


class CloneGroup:

    def __init__(self, parts, group_length, origin_part):
        self.parts: List[ClonePart] = parts
        self.group_length = group_length
        self.origin_part: ClonePart = origin_part

    def __str__(self):
        to_ret = ''
        for part in self.parts:
            to_ret = to_ret + str(part) + " - "
        to_ret += str(self.group_length)
        return to_ret

    def get__parts(self):
        return self.parts

    def get__group_length(self):
        return self.group_length

    def get__origin_part(self):
        return self.origin_part
