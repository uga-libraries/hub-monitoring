"""
Tests for the function save_accession_report(), which saves accession data to a CSV.
"""
import unittest
from collection_summary import save_accession_report
from test_script_collection_summary import csv_to_list
from datetime import datetime
from os import remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the report, if it was made by the tests"""
        today = datetime.today().strftime('%Y-%m-%d')
        path = join('test_data', f'hub-accession-summary_{today}.csv')
        if exists(path):
            remove(path)

    def test_header(self):
        """Test for making a new report with a header"""
        save_accession_report('test_data', 'header')

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join('test_data', f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        csv_made = exists(csv_path)
        self.assertEqual(csv_made, True, "Problem with test for header, CSV is made")

        # Verifies the CSV has the expected contents.
        result = csv_to_list(csv_path)
        expected = [['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                    'Moderate_Risk', 'Low_Risk', 'Notes']]
        self.assertEqual(result, expected, "Problem with test for header, CSV contents")

    def test_one_row(self):
        """Test for making a report with a header and one row of accession data"""
        save_accession_report('test_data', 'header')
        save_accession_report('test_data', ['2015-01-er', 'ms0001', 'backlog', '2015', 1.00, 111, 11, 15, 45, 40, ''])

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join('test_data', f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        csv_made = exists(csv_path)
        self.assertEqual(csv_made, True, "Problem with test for one row, CSV is made")

        # Verifies the CSV has the expected contents.
        result = csv_to_list(csv_path)
        expected = [['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                    'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['2015-01-er', 'ms0001', 'backlog', '2015', 1.00, 111, 11, 15, 45, 40, 'nan']]
        self.assertEqual(result, expected, "Problem with test for one row, CSV contents")

    def test_two_rows(self):
        """Test for making a report with a header and two rows of accession data"""
        save_accession_report('test_data', 'header')
        save_accession_report('test_data', ['2015-01-er', 'ms0001', 'backlog', '2015', 1.00, 111, 11, 15, 45, 40, ''])
        save_accession_report('test_data', ['2019-01-er', 'ms0001', 'backlog', '2019', 2.02, 200, 0, 0, 0, 0,
                                            'Accession 2019-01-er has no risk csv. '])

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join('test_data', f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        csv_made = exists(csv_path)
        self.assertEqual(csv_made, True, "Problem with test for two rows, CSV is made")

        # Verifies the CSV has the expected contents.
        result = csv_to_list(csv_path)
        expected = [['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['2015-01-er', 'ms0001', 'backlog', '2015', 1.00, 111, 11, 15, 45, 40, 'nan'],
                    ['2019-01-er', 'ms0001', 'backlog', '2019', 2.02, 200, 0, 0, 0, 0,
                     'Accession 2019-01-er has no risk csv. ']]
        self.assertEqual(result, expected, "Problem with test for two rows, CSV contents")


if __name__ == '__main__':
    unittest.main()
