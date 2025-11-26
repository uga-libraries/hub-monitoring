"""
Tests for the function check_completeness(), which looks for all four things that should be in an accession folder.
"""
import unittest
from accession_completeness_report import check_completeness
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_complete(self):
        """Test for an accession that is complete."""
        completeness_dict = check_completeness(join('test_data', 'check_completeness_test', 'coll_1', 'acc_1_1'))
        expected = {'pres_log': True, 'pres_log_format': None, 'full_risk': True,
                    'initial_manifest': True, 'bag': True}
        self.assertEqual(expected, completeness_dict, "Problem with test for complete")

    def test_not_complete(self):
        """Test for an accession that is missing all four required components."""
        completeness_dict = check_completeness(join('test_data', 'check_completeness_test', 'coll_1', 'acc_1_2'))
        expected = {'pres_log': False, 'pres_log_format': None, 'full_risk': False,
                    'initial_manifest': False, 'bag': False}
        self.assertEqual(expected, completeness_dict, "Problem with test for not complete")

    def test_pres_log_formatting(self):
        """Test for an accession with all four required components but the preservation log is formatted wrong."""
        completeness_dict = check_completeness(join('test_data', 'check_completeness_test', 'coll_1', 'acc_1_3'))
        expected = {'pres_log': False, 'pres_log_format': 'Nonstandard columns', 'full_risk': True,
                    'initial_manifest': True, 'bag': True}
        self.assertEqual(expected, completeness_dict, "Problem with test for pres log formatting")


if __name__ == '__main__':
    unittest.main()
