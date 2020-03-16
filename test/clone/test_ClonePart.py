import unittest
from detector.clone.ClonePart import ClonePart


class TestClonePart(unittest.TestCase):

    def test_clone_part_creation(self):
        file_name = "Test.java"
        unit_start = 0
        start_line = 0
        end_line = 4

        clone_part: ClonePart = ClonePart(file_name, unit_start, start_line, end_line)

        self.assertEqual(clone_part.get__filename(), file_name)
        self.assertEqual(clone_part.get__unit_start(), unit_start)
        self.assertEqual(clone_part.get__start_line(), start_line)
        self.assertEqual(clone_part.get__end_line(), end_line)


if __name__ == '__main__':
    unittest.main()
