"""
Tests for the function get_file_count(), which gets the number of files in a directory.
The directory may contain folders.
"""
import unittest
from collection_summary import get_file_count
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Path to the department hub, used in all tests."""
        self.dept_hub = join(getcwd(), '..', 'test_data', 'Collection_Summary', 'Russell_Hub')

    def test_file(self):
        """Test for a directory with one file and no folders"""
        acc_path = join(self.dept_hub, 'backlog', 'rbrl001', '2015-01-er')
        files = get_file_count(acc_path)
        self.assertEqual(files, 1, "Problem with test for one file")

    def test_file_folder(self):
        """Test for a directory with one file, which is in a folder"""
        acc_path = join(self.dept_hub, 'backlog', 'rbrl001', '2015-12-er')
        files = get_file_count(acc_path)
        self.assertEqual(files, 1, "Problem with test for one file in a folder")

    def test_files(self):
        """Test for a directory with two files and no folders"""
        acc_path = join(self.dept_hub, 'backlog', 'rbrl001', '2016-03-er')
        files = get_file_count(acc_path)
        self.assertEqual(files, 2, "Problem with test for two files")

    def test_files_folders(self):
        """Test for a directory with multiple files in multiple folders"""
        acc_path = join(self.dept_hub, 'backlog', 'rbrl001', '2018-04-er')
        files = get_file_count(acc_path)
        self.assertEqual(files, 5, "Problem with test for multiple files in multiple folders")

    def test_unbagged(self):
        """Test for an accession that is not in a bag"""
        acc_path = join(self.dept_hub, 'backlog', 'rbrl001', '2019-12-er')
        files = get_file_count(acc_path)
        self.assertEqual(files, 2, "Problem with test for unbagged")


if __name__ == '__main__':
    unittest.main()
