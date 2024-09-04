"""
Tests for the function check_completeness(), which looks for all four things that should be in an accession folder.
"""
import unittest
from accession_completeness_report import check_completeness
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_complete(self):
        """Test for an accession that is complete."""
        completeness_dict = check_completeness(join('check_completeness_test_data', 'coll_1', 'acc_1'))
        expected = {'pres_log': True, 'full_risk': True, 'initial_manifest': True, 'bag': True}
        self.assertEqual(completeness_dict, expected, "Problem with test for complete")

    def test_not_complete(self):
        """Test for an accession that is missing all four required components."""
        completeness_dict = check_completeness(join('check_completeness_test_data', 'coll_1', 'acc_2'))
        expected = {'pres_log': False, 'full_risk': False, 'initial_manifest': False, 'bag': False}
        self.assertEqual(completeness_dict, expected, "Problem with test for not complete")


if __name__ == '__main__':
    unittest.main()
