"""
Tests for the function most_recent_risk_csv(), which determines the most recent risk spreadsheet in a folder.
"""
import os
import unittest
from risk_update import most_recent_risk_csv


class MyTestCase(unittest.TestCase):

    def test_none(self):
        """Test for when there is no risk spreadsheet"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'no_spreadsheet'))
        expected = None
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for no spreadsheet')

    def test_one_dated(self):
        """Test for when there is one risk spreadsheet with a date"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'one_dated'))
        expected = '2001-01-er_full_risk_data_2001-01-15.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for one spreadsheet, with a date')

    def test_one_undated(self):
        """Test for when there is one risk spreadsheet without a date"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'one_undated'))
        expected = '2001-02-er_full_risk_data.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for one spreadsheet, undated')

    def test_two_both_dated(self):
        """Test for when there are two risk spreadsheets, both with dates"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'two_both_dated'))
        expected = '2002-01-er_full_risk_data_2017-10-31.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for two files, both with dates')

    def test_two_one_dated(self):
        """Test for when there are two risk spreadsheets, and only one has a date"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'two_one_undated'))
        expected = '2002-02-er_full_risk_data_2024-05-15.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for two files, one with a date')

    def test_three_all_dated(self):
        """Test for when there are three risk spreadsheets, all with dates, and a log (skipped)"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'three_all_dated'))
        expected = '2003-01-er_full_risk_data_2023-03-03.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for two files, both with dates')

    def test_three_one_undated(self):
        """Test for when there are three risk spreadsheets, two with dates"""
        risk_csv_filename = most_recent_risk_csv(os.path.join('test_data', 'most_recent_risk_csv', 'three_one_undated'))
        expected = '2003-02-er_full_risk_data_2013-02-28.csv'
        self.assertEqual(risk_csv_filename, expected, 'Problem with test for three files, two with dates')


if __name__ == '__main__':
    unittest.main()
