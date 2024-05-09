"""
Tests for the function accession_test(), which determines if a folder is an accession.
"""
import unittest
from collection_summary import accession_test


class MyTestCase(unittest.TestCase):

    def test_not_acc_1(self):
        """Test for when the folder does not match any accession patterns"""
        accession = 'AIPs V2'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, False, 'Problem with test for not accession 1')

    def test_not_acc_2(self):
        """Test for when the folder does not match any accession patterns"""
        accession = 'Risk_remediation'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, False, 'Problem with test for not accession 2')

    def test_pattern_1a(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and lowercase er"""
        accession = '2021-89-er'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1a')

    def test_pattern_1b(self):
        """Test for when the folder matches pattern 1 (year-number-er), with dashes and uppercase ER"""
        accession = '2022-19-ER'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1b')

    def test_pattern_1c(self):
        """Test for when the folder matches pattern 1 (year-number-er), with underscores and lowercase er"""
        accession = '2011_20_er'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1c')

    def test_pattern_1d(self):
        """Test for when the folder matches pattern 1 (year-number-er), with underscores and uppercase ER"""
        accession = '2013_36_ER'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1d')

    def test_pattern_1e(self):
        """Test for when the folder matches pattern 1 (year-number-er), with 3 digits instead of 2"""
        accession = '2022-108-er'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 1e')

    def test_pattern_2(self):
        """Test for when the folder matches pattern 2, equal to no-acc-num"""
        accession = 'no-acc-num'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 2')

    def test_pattern_3(self):
        """Test for when the folder matches pattern 3, letters_ER"""
        accession = 'MethvinE_ER'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 3')

    def test_pattern_4(self):
        """Test for when the folder matches pattern 4, ua##-###"""
        accession = 'ua16-010'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 4')

    def test_pattern_5(self):
        """Test for when the folder matches pattern 5, ua_##_###"""
        accession = 'ua_14_018'
        is_accession = accession_test(accession)
        self.assertEqual(is_accession, True, 'Problem with test for pattern 5')


if __name__ == '__main__':
    unittest.main()
