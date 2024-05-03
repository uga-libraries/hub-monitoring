"""
Tests for the function update_report(), which adds validation information to the script report.
"""
import unittest
from validate_fixity import update_report
from datetime import date
from os import getcwd, remove
from os.path import basename, exists, join
from pandas import read_csv


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the validation report, and accession reports for manifest validation, if made by any of the tests"""
        report = f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"
        if exists(report):
            remove(report)

    def test_bag_not_valid(self):
        """Test for adding validation information for bags that are not valid to an existing report"""
        # First call of the function to add a bag that is not valid.
        folder = '2023_test003_001_er'
        error = 'Payload-Oxum validation failed.'
        directory = getcwd()
        update_report(folder, error, directory)

        # Second call of the function to add another bag that is not valid.
        folder = '2023_test003_002_er'
        error = 'Bag validation failed.'
        directory = getcwd()
        update_report(folder, error, directory)

        # Verifies the fixity validation CSV has the correct values.
        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_001_er', 'Payload-Oxum validation failed.'],
                    ['2023_test003_002_er', 'Bag validation failed.']]
        self.assertEqual(report_rows, expected, 'Problem with test for bag not valid')

    def test_one_row(self):
        """Test for when the report is made for the first time"""
        # Call of the function to add a bag that is not valid.
        folder = '2023_test003_001_er'
        error = 'Bag validation failed.'
        directory = getcwd()
        update_report(folder, error, directory)

        # Verifies the fixity validation CSV has the correct values.
        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_001_er', 'Bag validation failed.']]
        self.assertEqual(report_rows, expected, 'Problem with test for one row')

    def test_manifest_not_valid(self):
        """Test for adding validation information for manifests that are not valid to an existing report"""
        # First call of the function to add a manifest that is not valid.
        root = join(getcwd(), '2023_test003_003_er')
        errors_list = [['error']]
        directory = getcwd()
        update_report(basename(root), f'{len(errors_list)} manifest errors', directory)

        # Second call of the function to add a manifest that is not valid.
        root = join(getcwd(), '2023_test003_004_er')
        errors_list = [['error'], ['error']]
        directory = getcwd()
        update_report(basename(root), f'{len(errors_list)} manifest errors', directory)

        # Verifies the fixity validation CSV has the correct values.
        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test003_003_er', '1 manifest errors'],
                    ['2023_test003_004_er', '2 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for manifest not valid')


if __name__ == '__main__':
    unittest.main()
