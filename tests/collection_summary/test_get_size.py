"""
Tests for the function get_size(), which gets the total size of the files in a directory, in GB.
The directory may contain folders
"""
import unittest
from collection_summary import get_size
from os.path import join


class MyTestCase(unittest.TestCase):
        
    def test_file(self):
        """Test for a directory with one file and no folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2022-27-er')
        size = get_size(acc_path)
        self.assertEqual(size, 0.00001, "Problem with test for one file")

    def test_file_folder(self):
        """Test for a directory with three files, some of which are in a folder"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-01-er')
        size = get_size(acc_path)
        self.assertEqual(size, 0.00001, "Problem with test one file in a folder")

    def test_files(self):
        """Test for a directory with two files and no folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-12-er')
        size = get_size(acc_path)
        self.assertEqual(size, 0.0001, "Problem with test for two files")

    def test_files_folders(self):
        """Test for a directory with multiple files and multiple folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-23-er')
        size = get_size(acc_path)
        self.assertEqual(size, 0.0005, "Problem with test for folder")

    def test_unbagged(self):
        """Test for an accession that is not in a bag"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        size = get_size(acc_path)
        self.assertEqual(size, 0.0002, "Problem with test for unbagged")


if __name__ == '__main__':
    unittest.main()
