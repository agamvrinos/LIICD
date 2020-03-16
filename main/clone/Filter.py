from typing import List
from clone.ClonePart import ClonePart
from clone.CloneGroup import CloneGroup


class Filter:
    """
    Filter clones fully covered by other clones.
    """

    NAME_COMPARATOR = 'NAME_COMPARATOR'
    NAME_UNIT_COMPARATOR = 'NAME_UNIT_COMPARATOR'

    def __init__(self):
        self.l1 = None
        self.l2 = None
        self.filtered: List[CloneGroup] = []

    def get__filtered(self):
        return self.filtered

    def add_in_filter(self, current_clone_group: CloneGroup):
        for earlier_clone_group in self.filtered:
            if self.contains_in(current_clone_group, earlier_clone_group):
                return
            if self.contains_in(earlier_clone_group, current_clone_group):
                self.filtered.remove(earlier_clone_group)

        self.filtered.append(current_clone_group)

    def contains_in(self, first: CloneGroup, second: CloneGroup):
        if first.get__group_length() > second.get__group_length():
            return False
        first_parts: List[ClonePart] = first.get__parts()
        second_parts: List[ClonePart] = second.get__parts()
        self.l1 = first.get__group_length()
        self.l2 = second.get__group_length()

        return self.contains(first_parts, second_parts, self.NAME_UNIT_COMPARATOR) and \
               self.contains(first_parts, second_parts, self.NAME_COMPARATOR)

    def contains(self, container: List[ClonePart], list1: List[ClonePart], comparator):
        container_index = 0
        list_index = 0

        while container_index < len(container) and list_index < len(list1):
            container_part: ClonePart = container[container_index]
            list_part: ClonePart = list1[list_index]

            if comparator == self.NAME_COMPARATOR:
                compare = self.compare_by_filename(container_part, list_part)
            else:
                compare = self.compare_by_filename_and_unit(container_part, list_part)

            if compare == 0:
                if list_index + 1 == len(list1):
                    return True
                list_index += 1
            elif compare < 0:
                if container_index + 1 == len(container):
                    return False
                container_index += 1
            else:
                return False

    def compare_by_filename(self, part1: ClonePart, part2: ClonePart):
        filename_1 = part1.get__filename()
        filename_2 = part2.get__filename()

        if filename_1 == filename_2:
            return 0
        elif filename_1 < filename_2:
            return -1
        else:
            return 1

    def compare_by_filename_and_unit(self, part1: ClonePart, part2: ClonePart):
        compare = self.compare_by_filename(part1, part2)

        if compare == 0:
            if part1.get__unit_start() <= part2.get__unit_start():
                if part2.get__unit_start() + self.l2 <= part1.get__unit_start() + self.l1:
                    return 0
                else:
                    return -1
            else:
                return 1
        else:
            return compare
