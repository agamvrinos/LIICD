import unittest
from typing import List
from detector.clone.ClonePart import ClonePart
from detector.clone.CloneGroup import CloneGroup


class TestCloneGroup(unittest.TestCase):

    def test_clone_group_creation(self):
        clone_parts: List[ClonePart] = [ClonePart("Test.java", 0, 0, 4)]
        group_length = 0
        origin_part = 0

        clone_group: CloneGroup = CloneGroup(clone_parts, group_length, origin_part)

        self.assertEqual(clone_group.get__parts(), clone_parts)
        self.assertEqual(clone_group.get__group_length(), group_length)
        self.assertEqual(clone_group.get__origin_part(), origin_part)


if __name__ == '__main__':
    unittest.main()
