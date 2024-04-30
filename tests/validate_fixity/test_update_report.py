"""
Tests for the function update_report(), which adds validation information to the script report.
"""
import unittest
from validate_fixity import update_report
from datetime import date
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the validation report, and accession reports for manifest validation, if made by any of the tests"""
        report = f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"
        if exists(report):
            remove(report)

    def test_bag_not_valid(self):
        """Test for adding validation information for bags that are not valid to an existing report"""
        update_report('2023_test003_001_er', 'Payload-Oxum validation failed.', getcwd())
        update_report('2023_test003_002_er', 'Bag validation failed.', getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_001_er', 'Payload-Oxum validation failed.'],
                    ['2023_test003_002_er', 'Bag validation failed.']]
        self.assertEqual(report_rows, expected, 'Problem with test for bag not valid')

    def test_one_row(self):
        """Test for when the report is made for the first time"""
        update_report('2023_test003_001_er', 'Bag validation failed.', getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_001_er', 'Bag validation failed.']]
        self.assertEqual(report_rows, expected, 'Problem with test for one row')

    def test_manifest_not_valid(self):
        """Test for adding validation information for manifests that are not valid to an existing report"""
        error_one = [['error']]
        update_report('2023_test003_003_er', f'{len(error_one)} manifest errors', getcwd())
        error_two = [['error'], ['error']]
        update_report('2023_test003_004_er', f'{len(error_two)} manifest errors', getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_003_er', '1 manifest errors'],
                    ['2023_test003_004_er', '2 manifest errors']]
        self.assertEqual(report_rows, expected, 'Problem with test for manifest not valid')


if __name__ == '__main__':
    unittest.main()
