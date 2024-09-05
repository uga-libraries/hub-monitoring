"""
Tests for the function accession_paths(), which finds the paths to every accession folder in a collection folder.
"""
import unittest
from accession_completeness_report import accession_paths
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_one_path(self):
        """Test for when there is one accession folder in the collection folder and nothing else"""
        coll_path = join('accession_paths_test_data', 'coll_1')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_1_1')]
        self.assertEqual(accession_list, expected, "Problem with test for one path")

    def test_multiple_paths(self):
        """Test for when there are three accession folders in the collection folder and nothing else"""
        coll_path = join('accession_paths_test_data', 'coll_2')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_2_1'), join(coll_path, 'acc_2_2'), join(coll_path, 'acc_2_3')]
        self.assertEqual(accession_list, expected, "Problem with test for multiple paths")

    def test_skip_file(self):
        """Test for when there is a file that will not be included within the collection folder,
        as well as one accession folder"""
        coll_path = join('accession_paths_test_data', 'coll_3')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_3_1')]
        self.assertEqual(accession_list, expected, "Problem with test for skip file")

    def test_skip_folders(self):
        """Test for when each of the skipped folder names are present in the collection folder,
        which should not be included, as well as two accession folders"""
        coll_path = join('accession_paths_test_data', 'coll_4')
        accession_list = accession_paths(coll_path)
        expected = [join(coll_path, 'acc_4_1'), join(coll_path, 'acc_4_2')]
        self.assertEqual(accession_list, expected, "Problem with test for skip folders")


if __name__ == '__main__':
    unittest.main()
