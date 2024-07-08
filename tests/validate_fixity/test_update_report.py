"""
Tests for the function update_report(), which adds validation information to the script report.

To simplify testing, the acc_dir paths do not exist. The test just needs something in path form to parse the data.
"""
import unittest
from validate_fixity import update_report
from test_script_validate_fixity import csv_to_list
from datetime import date
from os import getcwd, remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        if exists(f"fixity_validation_{today}.csv"):
            remove(f"fixity_validation_{today}.csv")

    def test_bag_not_valid(self):
        """Test for adding validation information for bags that are not valid to an existing report"""
        # First call of the function to add a bag that is not valid.
        bag_dir = join(getcwd(), 'backlogged', 'test_003', '2023_test003_001_er', '2023_test003_001_er_bag')
        errors = 'Payload-Oxum validation failed.'
        report_dir = getcwd()
        update_report(bag_dir, str(errors), report_dir)

        # Second call of the function to add another bag that is not valid.
        bag_dir = join(getcwd(), 'backlogged', 'test_003', '2023_test003_002_er', '2023_test003_002_er_bag')
        errors = 'Bag validation failed.'
        report_dir = getcwd()
        update_report(bag_dir, str(errors), report_dir)

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Validation_Error'],
                    ['backlogged', 'test_003', '2023_test003_001_er', 'Payload-Oxum validation failed.'],
                    ['backlogged', 'test_003', '2023_test003_002_er', 'Bag validation failed.']]
        self.assertEqual(result, expected, 'Problem with test for bag not valid')

    def test_one_row(self):
        """Test for when the report is made for the first time"""
        # Call of the function to add a bag that is not valid.
        bag_dir = join(getcwd(), 'backlogged', 'test_003', '2023_test003_001_er', '2023_test003_001_er_bag')
        errors = 'Bag validation failed.'
        report_dir = getcwd()
        update_report(bag_dir, str(errors), report_dir)

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Validation_Error'],
                    ['backlogged', 'test_003', '2023_test003_001_er', 'Bag validation failed.']]
        self.assertEqual(result, expected, 'Problem with test for one row')

    def test_manifest_not_valid(self):
        """Test for adding validation information for manifests that are not valid to an existing report"""
        # First call of the function to add a manifest that is not valid.
        acc_dir = join(getcwd(), 'closed', 'test_004', '2023_test004_003_er')
        error_list = [['error_msg']]
        report_dir = getcwd()
        update_report(acc_dir, f'{len(error_list)} manifest errors', report_dir)

        # Second call of the function to add a manifest that is not valid.
        acc_dir = join(getcwd(), 'closed', 'test_004', '2023_test004_004_er')
        error_list = [['error_msg'], ['error_msg']]
        report_dir = getcwd()
        update_report(acc_dir, f'{len(error_list)} manifest errors', report_dir)

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Validation_Error'],
                    ['closed', 'test_004', '2023_test004_003_er', '1 manifest errors'],
                    ['closed', 'test_004', '2023_test004_004_er', '2 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for manifest not valid')


if __name__ == '__main__':
    unittest.main()
