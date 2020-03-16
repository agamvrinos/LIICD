import unittest
from main.index.IndexEntry import IndexEntry
from main.index.CloneIndex import CloneIndex


class TestCloneIndex(unittest.TestCase):

    def setUp(self):
        self.clone_index = CloneIndex()
        self.clone_index.index_entries_by_file.clear()
        self.clone_index.index_entries_by_hash.clear()

        self.index_entry: IndexEntry = IndexEntry("Test.java", 0, "534FA5G", 0, 4)
        self.index_entry_2: IndexEntry = IndexEntry("Test.java", 1, "534FCCC", 1, 5)
        self.index_entry_3: IndexEntry = IndexEntry("Test2.java", 0, "534FA5G", 0, 4)

    def test_add_index_entry(self):
        self.assertTrue(len(self.clone_index.get__index_entries_by_file()) == 0)
        self.assertTrue(len(self.clone_index.get__index_entries_by_hash()) == 0)

        self.clone_index.add_index_entry(self.index_entry)
        self.assertTrue(len(self.clone_index.get__index_entries_by_file()) == 1)
        self.assertTrue(len(self.clone_index.get__index_entries_by_hash()) == 1)

    def test_get__index_entries_by_hash(self):
        self.clone_index.add_index_entry(self.index_entry)

        # the hash of the index entry added can be found as a key
        index_entries_by_hash = self.clone_index.get__index_entries_by_hash()
        self.assertTrue(index_entries_by_hash.get(self.index_entry.get__sequence_hash()) is not None)

        # index length does not increase when adding entry with the same hash
        self.clone_index.add_index_entry(self.index_entry_3)
        self.assertEqual(len(self.clone_index.get__index_entries_by_hash()), 1)

        # dictionary value length increases when adding entry with the same hash
        index_entries_by_hash = self.clone_index.get__index_entries_by_hash()
        self.assertEqual(len(index_entries_by_hash.get(self.index_entry.get__sequence_hash())), 2)

    def test_get__index_entries_by_file(self):
        self.clone_index.add_index_entry(self.index_entry)

        # the filename of the index entry added can be found as a key
        index_entries_by_file = self.clone_index.get__index_entries_by_file()
        self.assertTrue(index_entries_by_file.get(self.index_entry.get__file_name()) is not None)

        # index length does not increase when adding entry with the same filename
        self.clone_index.add_index_entry(self.index_entry_2)
        self.assertEqual(len(self.clone_index.get__index_entries_by_file()), 1)

        # dictionary value length increases when adding entry with the same filename
        index_entries_by_file = self.clone_index.get__index_entries_by_file()
        self.assertEqual(len(index_entries_by_file.get(self.index_entry.get__file_name())), 2)


if __name__ == '__main__':
    unittest.main()
