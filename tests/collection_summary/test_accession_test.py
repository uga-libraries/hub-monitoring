"""
Tests for the function accession_test(), which determines if a folder is an accession.
To simplify testing, the path (second function parameter) is to a real folder or file in test_data
but does not match the accession number being tested.
"""
import unittest
from collection_summary import accession_test
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_file(self):
        """Test for when it is a file instead of a folder"""
        accession = '2022-15-er_file_to_skip.txt'
        accession_dir =  join('test_data', 'Hargrett_Hub', 'backlogged', 'ms0001 Person papers', accession)
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, False, 'Problem with test for file')

    def test_not_acc_1(self):
        """Test for when the folder does not match any accession patterns"""
        accession = 'AIPs V2'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, False, 'Problem with test for not accession 1')

    def test_not_acc_2(self):
        """Test for when the folder does not match any accession patterns"""
        accession = 'Risk_remediation'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, False, 'Problem with test for not accession 2')

    def test_no_acc_num(self):
        """Test for when the folder is equal to no-acc-num"""
        accession = 'no-acc-num'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for no-acc-num')

    def test_pattern_1a(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and lowercase er"""
        accession = '2021-89-er'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1a')

    def test_pattern_1b(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and uppercase ER"""
        accession = '2022-19-ER'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1b')

    def test_pattern_1c(self):
        """Test for when the folder matches pattern 1 (year-number-er), with 3 digits instead of 2"""
        accession = '2022-108-er'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1c')

    def test_pattern_2a(self):
        """Test for when the folder matches pattern 2 (year-number-er), with underscores and lowercase er"""
        accession = '2011_20_er'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 2a')

    def test_pattern_2b(self):
        """Test for when the folder matches pattern 2 (year-number-er), with underscores and uppercase ER"""
        accession = '2013_36_ER'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 2b')

    def test_pattern_2c(self):
        """Test for when the folder matches pattern 2, letters_ER"""
        accession = 'MethvinE_ER'
        accession_dir = join('test_data', 'Russell_Hub', 'closed', 'rbrl003', '2019-13-er')
        is_accession = accession_test(accession, accession_dir)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 2c')


if __name__ == '__main__':
    unittest.main()
