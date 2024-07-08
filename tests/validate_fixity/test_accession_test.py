"""
Tests for the function accession_test(), which determines if a folder is an accession.
"""
import unittest
from validate_fixity import accession_test


class MyTestCase(unittest.TestCase):

    def test_not_acc_1(self):
        """Test for when the folder does not match any accession patterns"""
        folder = 'coll123er000001_bag'
        result = accession_test(folder)
        self.assertEqual(result, False, 'Problem with test for not accession 1')

    def test_not_acc_2(self):
        """Test for when the folder does not match any accession patterns"""
        folder = 'Risk Remediation_bag'
        result = accession_test(folder)
        self.assertEqual(result, False, 'Problem with test for not accession 2')

    def test_no_acc_num(self):
        """Test for when the folder is equal to no-acc-num"""
        folder = 'no-acc-num_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for no-acc-num')

    def test_pattern_1a(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and lowercase er"""
        folder = '2021-89-er_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 1a')

    def test_pattern_1b(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and uppercase ER"""
        folder = '2022-19-ER_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 1b')

    def test_pattern_1c(self):
        """Test for when the folder matches pattern 1 (year-number-er), with 3 digits instead of 2"""
        folder = '2022-108-er_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 1c')

    def test_pattern_2a(self):
        """Test for when the folder matches pattern 2 (year-number-er), with underscores and lowercase er"""
        folder = '2011_20_er_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 2a')

    def test_pattern_2b(self):
        """Test for when the folder matches pattern 2 (year-number-er), with underscores and uppercase ER"""
        folder = '2013_36_ER_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 2b')

    def test_pattern_2c(self):
        """Test for when the folder matches pattern 2, letters_ER"""
        folder = 'MethvinE_ER_bag'
        result = accession_test(folder)
        self.assertEqual(result, True, 'Problem with test for pattern 2c')


if __name__ == '__main__':
    unittest.main()
