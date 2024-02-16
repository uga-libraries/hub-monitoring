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
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-01-er')
        files = get_file_count(path)
        self.assertEqual(files, 3, "Problem with test for folder")

    def test_one_file(self):
        """Test for a directory with one file and no folders"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl001', '2021-01-er')
        files = get_file_count(path)
        self.assertEqual(files, 1, "Problem with test for one file")

    def test_two_files(self):
        """Test for a directory with two files and no folders"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-01-er')
        files = get_file_count(path)
        self.assertEqual(files, 2, "Problem with test for two files")


if __name__ == '__main__':
    unittest.main()
