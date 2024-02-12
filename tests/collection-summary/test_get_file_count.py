"""
Tests for the function get_file_count(), which gets the number of files in a directory.
The directory may contain folders.
"""
import unittest
from collection_summary import get_file_count
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_folder(self):
        """Test for a directory with three files, some of which are in a folder"""
        path = join(getcwd(), '..', 'test_data', 'closed', 'coll-003', '2023-01')
        files = get_file_count(path)
        self.assertEqual(files, 5, "Problem with test for folder")

    def test_one_file(self):
        """Test for a directory with one file and no folders"""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-001', '2021-01')
        files = get_file_count(path)
        self.assertEqual(files, 3, "Problem with test for one file")

    def test_two_files(self):
        """Test for a directory with two files and no folders"""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-002', '2022-01')
        files = get_file_count(path)
        self.assertEqual(files, 4, "Problem with test for two files")


if __name__ == '__main__':
    unittest.main()
