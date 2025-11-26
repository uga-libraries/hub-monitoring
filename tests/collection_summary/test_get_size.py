"""
Tests for the function get_size(), which gets the total size of the files (in GB) and number of files in a bag.
"""
import unittest
from collection_summary import get_size
from os.path import join


class MyTestCase(unittest.TestCase):
        
    def test_bag(self):
        """Test for an accession that is in a bag (size is calculated)"""
        acc_path = join('test_data', 'Russell_Hub', 'born-digital', 'closed', 'rbrl003', '2023-23-er')
        files, size_gb, size_error = get_size(acc_path)
        self.assertEqual(8, files, "Problem with test for bag, files")
        self.assertEqual(0.0005, size_gb, "Problem with test for bag, size_gb")
        self.assertEqual(None, size_error, 'Problem with test for bag, size_error')

    def test_no_bag(self):
        """Test for an accession that is not in a bag (size is not calculated)"""
        acc_path = join('test_data', 'Russell_Hub', 'born-digital', 'closed', 'rbrl003', '2019-13-er')
        files, size_gb, size_error = get_size(acc_path)
        self.assertEqual(0, files, "Problem with test for no_bag, files")
        self.assertEqual(0, size_gb, "Problem with test for no_bag, size_gb")
        self.assertEqual('Accession bag not found', size_error, 'Problem with test for no_bag, size_error')


if __name__ == '__main__':
    unittest.main()
