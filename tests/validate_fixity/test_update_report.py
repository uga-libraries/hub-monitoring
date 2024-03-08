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

    def test_header(self):
        """Test for when the report is made for the first time and the header is added"""
        update_report(['Bag', 'Errors'], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Bag', 'Errors']]
        self.assertEqual(report_rows, expected, 'Problem with test for header')

    def test_validation(self):
        """Test for when validation information for a bag is added to an existing report"""
        update_report(['Bag', 'Errors'], getcwd())
        update_report(['2023_test003_001_er', 'Payload-Oxum validation failed.'], getcwd())
        update_report(['2023_test003_002_er', 'Bag valid'], getcwd())

        df = read_csv(join(getcwd(), f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Bag', 'Errors'],
                    ['2023_test003_001_er', 'Payload-Oxum validation failed.'],
                    ['2023_test003_002_er', 'Bag valid']]
        self.assertEqual(report_rows, expected, 'Problem with test for validation')


if __name__ == '__main__':
    unittest.main()
