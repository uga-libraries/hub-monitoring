"""
Tests for the function most_recent_risk_csv(), which determines the most recent risk spreadsheet in a folder.
"""
import unittest
from risk_update import most_recent_risk_csv


class MyTestCase(unittest.TestCase):

    def test_1(self):
        """Test for when there is one preservation spreadsheet without a date"""
        files = ['2000-01-er_full_risk_data.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data.csv'
        self.assertEqual(file, expected, 'Problem with test for one spreadsheet, no date')

    def test_1_date(self):
        """Test for when there is one preservation spreadsheet with a date"""
        files = ['2000-01-er_full_risk_data_2003-02-15.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data_2003-02-15.csv'
        self.assertEqual(file, expected, 'Problem with test for one spreadsheet, with a date')

    def test_2(self):
        """Test for when there are two preservation spreadsheets, and only one has a date"""
        files = ['2000-01-er_full_risk_data.csv', '2000-01-er_full_risk_data_2003-02-15.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data_2003-02-15.csv'
        self.assertEqual(file, expected, 'Problem with test for two files, one with a date')

    def test_2_dates(self):
        """Test for when there are two preservation spreadsheets, both with dates."""
        files = ['2000-01-er_full_risk_data_2000-01-31.csv', '2000-01-er_full_risk_data_2003-02-15.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data_2003-02-15.csv'
        self.assertEqual(file, expected, 'Problem with test for two files, both with dates')

    def test_3(self):
        """Test for when there are three preservation spreadsheets, two with dates."""
        files = ['2000-01-er_full_risk_data_2003-02-16.csv', '2000-01-er_full_risk_data_2003-02-15.csv',
                 '2000-01-er_full_risk_data.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data_2003-02-16.csv'
        self.assertEqual(file, expected, 'Problem with test for three files, two with dates')

    def test_3_dates(self):
        """Test for when there are three preservation spreadsheets, all with dates."""
        files = ['2000-01-er_full_risk_data_2000-01-31.csv', '2000-01-er_full_risk_data_2004-02-15.csv',
                 '2000-01-er_full_risk_data_2003-02-15.csv', 'log.txt']
        file = most_recent_risk_csv(files)
        expected = '2000-01-er_full_risk_data_2004-02-15.csv'
        self.assertEqual(file, expected, 'Problem with test for two files, both with dates')


if __name__ == '__main__':
    unittest.main()
