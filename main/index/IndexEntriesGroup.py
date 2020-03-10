from typing import List
from index import IndexEntry


class IndexEntriesGroup:

    def __init__(self, index_entries=None):
        if index_entries is None:
            index_entries = []
        self.index_entries_group = index_entries

    def __str__(self):
        to_ret = ""
        for index_entry in self.index_entries_group:
            to_ret += str(index_entry) + "\n"
        return to_ret

    def get__index_entries_group(self):
        return self.index_entries_group

    def get__size(self):
        return len(self.index_entries_group)

    def get__first(self, filename):
        for entry in self.index_entries_group:
            if entry.get__file_name() == filename:
                return entry
        return None

    def get__pairs(self, group, length):
        i = 0
        j = 0
        result: List[IndexEntry] = []
        begin_group: List[IndexEntry] = self.index_entries_group
        end_group: List[IndexEntry] = group.get__index_entries_group()

        while i < len(begin_group) and j < len(end_group):
            begin_group_entry: IndexEntry = begin_group[i]
            end_group_entry: IndexEntry = end_group[j]
            begin_group_entry_filename = begin_group_entry.get__file_name()
            end_group_entry_filename = end_group_entry.get__file_name()

            if begin_group_entry_filename > end_group_entry_filename:
                idx = 1
            elif begin_group_entry_filename < end_group_entry_filename:
                idx = -1
            else:
                idx = begin_group_entry.get__statement_index() + length - 1 - end_group_entry.get__statement_index()

            if idx == 0:
                result.append([begin_group_entry, end_group_entry])
                i += 1
                j += 1
            elif idx > 0:
                j += 1
            else:
                i += 1

        return result

    def add_entry(self, index_entry):
        self.index_entries_group.append(index_entry)

    def extend(self, index_entries_to_append):
        self.index_entries_group.extend(index_entries_to_append)

    def subset_of(self, prev_group, index_correction=1):
        i = 0
        j = 0
        current_group = self.index_entries_group
        other_group = prev_group.get__index_entries_group()

        while i < len(current_group) and j < len(other_group):
            current_group_entry = current_group[i]
            previous_group_entry = other_group[j]
            current_group_entry_filename = current_group_entry.get__file_name()
            previous_group_entry_filename = previous_group_entry.get__file_name()

            if current_group_entry_filename != previous_group_entry_filename:
                j += 1
                continue

            idx = current_group_entry.get__statement_index() - index_correction - previous_group_entry.get__statement_index()

            if idx < 0:
                break
            if idx != 0:
                j += 1
            else:
                j += 1
                i += 1

        return i == len(current_group)

    def intersect(self, group):
        i = 0
        j = 0
        intersection_group = IndexEntriesGroup()
        current_group: List[IndexEntry] = self.index_entries_group
        other_group: List[IndexEntry] = group.get__index_entries_group()

        while i < len(current_group) and j < len(other_group):
            current_group_entry = current_group[i]
            other_group_entry = other_group[j]
            current_group_entry_filename = current_group_entry.get__file_name()
            other_group_entry_filename = other_group_entry.get__file_name()

            if current_group_entry_filename > other_group_entry_filename:
                j += 1
                continue
            if current_group_entry_filename < other_group_entry_filename:
                i += 1
                continue

            idx = current_group_entry.get__statement_index() + 1 - other_group_entry.get__statement_index()

            if idx == 0:
                i += 1
                j += 1
                intersection_group.add_entry(other_group_entry)
            elif idx > 0:
                j += 1
            else:
                i += 1

        return intersection_group
