"""
Tests for the function save_risk_csv(), which save the updated risk information to a CSV.

To simplify the test, the new_risk_df is made within the test and only has a few of the columns.
"""
import unittest
from risk_update import save_risk_csv
from test_script_risk_update import csv_to_list
from datetime import datetime
from os import remove
from os.path import exists, join
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the test output if it was created"""
        today = datetime.today().strftime('%Y-%m-%d')
        if exists(join('test_data', 'script_new', 'rbrl004', '2005-10-er', f'2005-10-er_full_risk_data_{today}.csv')):
            remove(join('test_data', 'script_new', 'rbrl004', '2005-10-er', f'2005-10-er_full_risk_data_{today}.csv'))

    def test_duplicates(self):
        """Test for when the risk information includes duplicate rows"""
        # Creates input variables and runs the function.
        root = join('test_data', 'script_new', 'rbrl004', '2005-10-er')
        new_risk_df = DataFrame([['Word', 'NO VALUE', 'No Match'],
                                 ['Word', 'NO VALUE', 'No Match'],
                                 ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'Low Risk'],
                                 ['Rich Text Format', '1.6', 'Low Risk'],
                                 ['Rich Text Format', '1.6', 'Low Risk'],
                                 ['Rich Text Format', '1.6', 'Low Risk'],
                                 ['HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'Low Risk']],
                                columns=['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'])
        save_risk_csv(root, new_risk_df)

        # Tests the contents of the csv are correct.
        result = csv_to_list(join(root, f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'],
                    ['Word', 'NO VALUE', 'No Match'],
                    ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'Low Risk'],
                    ['Rich Text Format', '1.6', 'Low Risk'],
                    ['HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'Low Risk']]
        self.assertEqual(result, expected, 'Problem with test for duplicates')

    def test_no_duplicates(self):
        """Test for when the risk information includes no duplicate rows"""
        # Creates input variables and runs the function.
        root = join('test_data', 'script_new', 'rbrl004', '2005-10-er')
        new_risk_df = DataFrame([['Word', 'NO VALUE', 'No Match'],
                                 ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'Low Risk'],
                                 ['Rich Text Format', '1.6', 'Low Risk'],
                                 ['HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'Low Risk']],
                                columns=['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'])
        save_risk_csv(root, new_risk_df)

        # Tests the contents of the csv are correct.
        result = csv_to_list(join(root, f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'],
                    ['Word', 'NO VALUE', 'No Match'],
                    ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'Low Risk'],
                    ['Rich Text Format', '1.6', 'Low Risk'],
                    ['HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'Low Risk']]
        self.assertEqual(result, expected, 'Problem with test for duplicates')


if __name__ == '__main__':
    unittest.main()
