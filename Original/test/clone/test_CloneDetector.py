import unittest
from typing import List
from detector.index.IndexEntry import IndexEntry
from detector.index.CloneIndex import CloneIndex
from detector.clone.CloneGroup import CloneGroup
from detector.clone.CloneDetector import CloneDetector


class TestCloneGroup(unittest.TestCase):

    CHUNK_LENGTH = 5

    def setUp(self):
        self.test_clone_index = CloneIndex()
        self.test_clone_index.index_entries_by_file = {}
        self.test_clone_index.index_entries_by_hash = {}

    def test_no_clones(self):
        """
        Tests that the detector does not detect any clones if there aren't any
        clones to detect in the first place.

        Input:
            x: h0 h1
            y: h2 h3
        """
        index_entries_x = self.generate_entries("x", 2, 0)
        self.test_clone_index.add_index_entries(index_entries_x)

        new_file_index_entries = self.generate_entries("y", 2, 2)

        detector = CloneDetector(self.test_clone_index)
        results: List[CloneGroup] = detector.detect_clones(new_file_index_entries)

        self.assertEqual(len(results), 0, "should result in 0 clones")

    def test_multi_file_clones(self):
        """
        Tests that the detector detects correctly clones between multiple files.
        Input:
            x:    h1 h2 h3
            y:    h1 h2
            z: h0 h1 h2
        Expected:
            x - y - z => h1 h2
        """
        index_entries_x = self.generate_entries("x", 3, 1)
        index_entries_y = self.generate_entries("y", 2, 1)
        index_entries_y.extend(index_entries_x)

        self.test_clone_index.add_index_entries(index_entries_y)

        new_file_index_entries = self.generate_entries("z", 3, 0)

        detector = CloneDetector(self.test_clone_index)
        results: List[CloneGroup] = detector.detect_clones(new_file_index_entries)

        self.assertEqual(len(results), 1, "should result in 1 clone")

        group = results[0]
        print(group)

        parts = group.get__parts()
        length = group.get__group_length()

        self.assertEqual(len(parts), 3, "should consist of 3 parts representing the 3 files")
        self.assertEqual(length, 2, "maximum clone should be a combination of 2 clone groups")

    def test_multi_file_multi_clones(self):
        """
        Tests that the detector detects correctly multiple clones between multiple
        files.
        Input:
            x:    h1 h2 h3 h4
            y:       h2 h3
            z: h0 h1 h2 h3 h4 h5
        Expected:
            x - z => h1 h2 h3 h4
            x - y - z => h2 h3
        """
        index_entries_x = self.generate_entries("x", 4, 1)
        index_entries_y = self.generate_entries("y", 2, 2)
        index_entries_y.extend(index_entries_x)

        self.test_clone_index.add_index_entries(index_entries_y)

        new_file_index_entries = self.generate_entries("z", 6, 0)

        detector = CloneDetector(self.test_clone_index)
        results: List[CloneGroup] = detector.detect_clones(new_file_index_entries)

        self.assertEqual(len(results), 2, "should result in 2 clones")

        clone_2_pairs = results[0]
        self.assertEqual(len(clone_2_pairs.get__parts()), 2, "should consist of 2 parts representing the clones "
                                                             "between files \"x\" and \"z\"")
        self.assertEqual(clone_2_pairs.get__group_length(), 4, "maximum clone should be a combination of 4 clone groups")

        clone_3_pairs = results[1]
        self.assertEqual(len(clone_3_pairs.get__parts()), 3, "should consist of 3 parts representing the clones "
                                                             "between files \"x\", \"y\" and \"z\"")
        self.assertEqual(clone_3_pairs.get__group_length(), 2, "maximum clone should be a combination of 2 clone groups")

    def generate_entries(self, filename, count, from_index):
        index_entries = []
        for i in range(0, count):
            entry = IndexEntry(filename, i, "hash" + str(from_index + i), i, i + self.CHUNK_LENGTH)
            index_entries.append(entry)
        return index_entries


if __name__ == '__main__':
    unittest.main()
