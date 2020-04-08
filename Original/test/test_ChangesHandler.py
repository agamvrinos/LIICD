import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from detector.index.IndexEntry import IndexEntry
from detector.index.CloneIndex import CloneIndex
from detector.clone.CloneDetector import CloneDetector
from detector.ChangesHandler import ChangesHandler
from detector.CodebaseReader import CodebaseReader


class TestChangesHandler(unittest.TestCase):

    CHUNK_LENGTH = 5

    @classmethod
    def setUpClass(cls):
        index_entries_x = cls.generate_entries("x.java", 2, 0)
        cls.test_clone_index = CloneIndex()
        cls.test_clone_index.index_entries_by_file.clear()
        cls.test_clone_index.index_entries_by_hash.clear()

        cls.test_clone_index.add_index_entries(index_entries_x)

        cls.detector = CloneDetector(cls.test_clone_index)

    @patch.object(CodebaseReader, 'get_lines_for_file')
    def test_files_creation_handler(self, get_lines_for_file):
        """
        Initial index state:
            x:  h0 h1
        Final index state
            x:  h0 h1
            y:  h2 h3
        """
        creates_lst = ["y.java"]
        changes_handler = ChangesHandler(self.detector, [], [], creates_lst)

        # test the initial clone index size contains entries for 1 file
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 1)
        # test the initial hash entries of the index by hash dict are correct
        self.assertTrue("hash0" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash1" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash2" not in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" not in list(self.test_clone_index.get__index_entries_by_hash().keys()))

        # mock "get_lines_for_file" call
        get_lines_for_file.return_value = []

        created_file_entries = self.generate_entries("y.java", 2, 2)
        self.detector.clone_index.calculate_index_entries_for_file = MagicMock(return_value=created_file_entries)

        changes_handler.handle_changes()

        # test that the size of the index by file has increased
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 2)
        # test that a new entry has been added in the index by file dict
        self.assertTrue(creates_lst[0] in list(self.test_clone_index.get__index_entries_by_file().keys()))
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()[creates_lst[0]]), 2)
        # test that the size of the index by hash has increased
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_hash()), 4)
        # test that new hash entries have been added in the index by hash dict
        self.assertTrue("hash2" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" in list(self.test_clone_index.get__index_entries_by_hash().keys()))

    def test_files_deletion_handler(self):
        """
        Initial index state:
            x:  h0 h1
            y:  h2 h3
        Final index state
            y:  h2 h3
        """
        deletes_lst = ["x.java"]
        changes_handler = ChangesHandler(self.detector, deletes_lst, [], [])

        # test the initial clone index size contains entries for 2 files (after creation)
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 2)
        # test the initial hash entries of the index by hash dict are correct
        self.assertTrue("hash0" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash1" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash2" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" in list(self.test_clone_index.get__index_entries_by_hash().keys()))

        changes_handler.handle_changes()

        # test that the size of the index by file has decreased
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 1)
        # test the correct file was deleted from the index by file dict
        self.assertTrue(deletes_lst[0] not in list(self.test_clone_index.get__index_entries_by_file().keys()))
        # test the correct hash entries were removed from the index by hash dict
        self.assertTrue("hash0" not in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash1" not in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash2" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" in list(self.test_clone_index.get__index_entries_by_hash().keys()))

    @patch.object(CodebaseReader, 'get_lines_for_file')
    def test_files_update_handler(self, get_lines_for_file):
        """
        Initial index state:
            y:  h2 h3
        Final index state
            y:  h0 h1 h2
        """
        updates_lst = ["y.java"]
        changes_handler = ChangesHandler(self.detector, [], updates_lst, [])

        # test the initial clone index size contains entries for 1 file
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 1)
        self.assertTrue(updates_lst[0] in list(self.test_clone_index.get__index_entries_by_file().keys()))
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()[updates_lst[0]]), 2)
        # test the initial hash entries of the index by hash dict are correct
        self.assertTrue("hash2" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" in list(self.test_clone_index.get__index_entries_by_hash().keys()))

        # mock "get_lines_for_file" call
        get_lines_for_file.return_value = []

        updated_file_entries = self.generate_entries("y.java", 3, 0)
        self.detector.clone_index.calculate_index_entries_for_file = MagicMock(return_value=updated_file_entries)

        changes_handler.handle_changes()

        # test the clone index size does not change
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()), 1)
        self.assertTrue(updates_lst[0] in list(self.test_clone_index.get__index_entries_by_file().keys()))
        self.assertEqual(len(self.test_clone_index.get__index_entries_by_file()[updates_lst[0]]), 3)
        # test the correct hash entries were removed from the index by hash dict
        self.assertTrue("hash0" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash1" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash2" in list(self.test_clone_index.get__index_entries_by_hash().keys()))
        self.assertTrue("hash3" not in list(self.test_clone_index.get__index_entries_by_hash().keys()))

    @classmethod
    def generate_entries(cls, filename, count, from_index):
        index_entries = []
        for i in range(0, count):
            entry = IndexEntry(filename, i, "hash" + str(from_index + i), i, i + cls.CHUNK_LENGTH)
            index_entries.append(entry)
        return index_entries


if __name__ == '__main__':
    unittest.main()
