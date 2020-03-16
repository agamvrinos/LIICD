import unittest
from main.index.IndexEntry import IndexEntry


class TestIndexEntry(unittest.TestCase):

    def test_index_creation(self):
        file_name = "Test.java"
        statement_index = 0
        sequence_hash = "534FA5G"
        start_line = 0
        end_line = 4

        index_entry: IndexEntry = IndexEntry(file_name, statement_index, sequence_hash, start_line, end_line)
        self.assertEqual(index_entry.get__file_name(), file_name, "Filename should be " + file_name)
        self.assertEqual(index_entry.get__statement_index(), statement_index, "Statement index should be " + str(statement_index))
        self.assertEqual(index_entry.get__sequence_hash(), sequence_hash, "Sequence hash should be " + sequence_hash)
        self.assertEqual(index_entry.get__start_line(), start_line, "Start line should be " + str(statement_index))
        self.assertEqual(index_entry.get__end_line(), end_line, "End line should be " + str(statement_index))


if __name__ == '__main__':
    unittest.main()
