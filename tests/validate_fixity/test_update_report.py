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
        """Delete the validation report, if it is made by any of the tests"""
        report = f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"
        if exists(report):
            remove(report)

    def test_bag_not_valid(self):
        """Test for adding validation information for bags that are not valid to an existing report"""
        update_report(['Accession', 'Valid', 'Errors'], getcwd())
        update_report(['2023_test003_001_er', False, 'Payload-Oxum validation failed.'], getcwd())
        update_report(['2023_test003_002_er', False, 'Bag validation failed.'], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        df = df.fillna('nan')
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors'],
                    ['2023_test003_001_er', False, 'Payload-Oxum validation failed.'],
                    ['2023_test003_002_er', False, 'Bag validation failed.']]
        self.assertEqual(report_rows, expected, 'Problem with test for validation')

    def test_bag_valid(self):
        """Test for adding validation information for bags that are valid to an existing report"""
        update_report(['Accession', 'Valid', 'Errors'], getcwd())
        update_report(['2023_test003_001_er', True, None], getcwd())
        update_report(['2023_test003_002_er', True, None], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        df = df.fillna('nan')
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors'],
                    ['2023_test003_001_er', True, 'nan'],
                    ['2023_test003_002_er', True, 'nan']]
        self.assertEqual(report_rows, expected, 'Problem with test for validation')

    def test_header(self):
        """Test for when the report is made for the first time and the header is added"""
        update_report(['Accession', 'Valid', 'Errors'], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors']]
        self.assertEqual(report_rows, expected, 'Problem with test for header')

    def test_valid_mix(self):
        """Test for adding validation information for bags that are and are not valid to an existing report"""
        update_report(['Accession', 'Valid', 'Errors'], getcwd())
        update_report(['2023_test003_001_er', False, 'Payload-Oxum validation failed.'], getcwd())
        update_report(['2023_test003_002_er', True, None], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        df = df.fillna('nan')
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors'],
                    ['2023_test003_001_er', False, 'Payload-Oxum validation failed.'],
                    ['2023_test003_002_er', True, 'nan']]
        self.assertEqual(report_rows, expected, 'Problem with test for validation')


if __name__ == '__main__':
    unittest.main()
