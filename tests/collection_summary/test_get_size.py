"""
Tests for the function get_size(), which gets the number of files and total size of the files (in GB) in a directory.
The directory may contain folders.
"""
import unittest
from collection_summary import get_size
from os.path import join


class MyTestCase(unittest.TestCase):
        
    def test_file(self):
        """Test for a directory with one file and no folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2022-27-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 1, "Problem with test for one file, files")
        self.assertEqual(size_gb, 0.00001, "Problem with test for one file, size_gb")

    def test_file_folder(self):
        """Test for a directory with one file, which is in a folder"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-01-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 1, "Problem with test for one file in a folder, files")
        self.assertEqual(size_gb, 0.00001, "Problem with test one file in a folder, size_gb")

    def test_files(self):
        """Test for a directory with two files and no folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-12-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 2, "Problem with test for two files, files")
        self.assertEqual(size_gb, 0.0001, "Problem with test for two files, size_gb")

    def test_files_folders(self):
        """Test for a directory with multiple files and multiple folders"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2023-23-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 8, "Problem with test for folder, files")
        self.assertEqual(size_gb, 0.0005, "Problem with test for folder, size_gb")

    def test_no_bag(self):
        """Test for an accession that is not in a bag"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 6, "Problem with test for no bag, files")
        self.assertEqual(size_gb, 0.0002, "Problem with test for no bag, size_gb")

    def test_organization_error(self):
        """Test for an accession that is not organized in an expected way and cannot calculate size"""
        acc_path = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2024-31-er')
        files, size_gb = get_size(acc_path)
        self.assertEqual(files, 0, "Problem with test for organization error, files")
        self.assertEqual(size_gb, 0, "Problem with test for organization error, size_gb")

    # def test_file_not_found_error(self):
    #     """Template for test for when the path length is too long to calculate size
    #     This is caused by path length and cannot be reliably replicated in the test data.
    #     Instead, supply the path to an accession known to have this error.
    #     """
    #     # Makes variables for function input and runs the function.
    #     acc_path = r'INSERT PATH TO ACCESSION FOLDER'
    #     files, size_gb = get_size(acc_path)
    #     self.assertEqual(files, 0, "Problem with test for file not found error, files")
    #     self.assertEqual(size_gb, 0, "Problem with test for file not found error, size_gb")


if __name__ == '__main__':
    unittest.main()
