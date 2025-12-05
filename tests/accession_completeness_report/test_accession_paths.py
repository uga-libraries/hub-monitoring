"""
Tests for the function accession_paths(), which finds the paths to every accession folder in a collection folder.
"""
import unittest
from accession_completeness_report import accession_paths
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_one_path(self):
        """Test for when there is one accession folder in the collection folder and nothing else"""
        coll_path = join('test_data', 'accession_paths', 'coll_1')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_1_1')]
        self.assertEqual(expected, accession_list, "Problem with test for one path")

    def test_multiple_paths(self):
        """Test for when there are three accession folders in the collection folder and nothing else"""
        coll_path = join('test_data', 'accession_paths', 'coll_2')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_2_1'), join(coll_path, 'acc_2_2'), join(coll_path, 'acc_2_3')]
        self.assertEqual(expected, accession_list, "Problem with test for multiple paths")

    def test_skip_file(self):
        """Test for when there is a file that will not be included within the collection folder,
        as well as one accession folder"""
        coll_path = join('test_data', 'accession_paths', 'coll_3')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_3_1')]
        self.assertEqual(expected, accession_list, "Problem with test for skip file")

    def test_skip_endswith(self):
        """Test for when accession_FITS that should not be included is present"""
        coll_path = join('test_data', 'accession_paths', 'coll_4')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_4_1'), join(coll_path, 'acc_4_2')]
        self.assertEqual(expected, accession_list, "Problem with test for skip endswith")

    def test_skip_equal(self):
        """Test for when each of the folder names that should not be included is present"""
        coll_path = join('test_data', 'accession_paths', 'coll_5')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_5_1')]
        self.assertEqual(expected, accession_list, "Problem with test for skip equal")

    def test_skip_startswith(self):
        """Test for when each of the prefixes for folder names that should not be included is present"""
        coll_path = join('test_data', 'accession_paths', 'coll_6')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_6_1')]
        self.assertEqual(expected, accession_list, "Problem with test for skip startswith")


if __name__ == '__main__':
    unittest.main()
