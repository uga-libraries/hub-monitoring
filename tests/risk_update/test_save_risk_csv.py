"""
Tests for the function save_risk_csv(), which save the updated risk information to a CSV.

To simplify the test, the new_risk_df is made within the test and only has a few of the columns.
"""
from datetime import date
import os
import pandas as pd
import unittest
from risk_update import save_risk_csv
from test_script_risk_update import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the test output if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        if os.path.exists(os.path.join('test_data', f'test_data_full_risk_data_{today}.csv')):
            os.remove(os.path.join('test_data', f'test_data_full_risk_data_{today}.csv'))

    def test_duplicates(self):
        """Test for when the risk information includes duplicate rows"""
        # Creates input variable and runs the function.
        new_risk_df = pd.DataFrame([['Word', 'NO VALUE', 'No Match'],
                                    ['Word', 'NO VALUE', 'No Match'],
                                    ['PDF/A-1a', 'NO VALUE', 'Low Risk'],
                                    ['Rich Text', '1.6', 'Low Risk'],
                                    ['Rich Text', '1.6', 'Low Risk'],
                                    ['Rich Text', '1.6', 'Low Risk'],
                                    ['HTML', 'NO VALUE', 'Low Risk']],
                                   columns=['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'])
        save_risk_csv('test_data', new_risk_df)

        # Tests the contents of the csv are correct.
        result = csv_to_list(os.path.join('test_data', f"test_data_full_risk_data_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'],
                    ['Word', 'NO VALUE', 'No Match'],
                    ['PDF/A-1a', 'NO VALUE', 'Low Risk'],
                    ['Rich Text', '1.6', 'Low Risk'],
                    ['HTML', 'NO VALUE', 'Low Risk']]
        self.assertEqual(result, expected, 'Problem with test for duplicates')

    def test_no_duplicates(self):
        """Test for when the risk information includes no duplicate rows"""
        # Creates input variables and runs the function.
        new_risk_df = pd.DataFrame([['Word', 'NO VALUE', 'No Match'],
                                    ['PDF/A-1a', 'NO VALUE', 'Low Risk'],
                                    ['Rich Text', '1.6', 'Low Risk'],
                                    ['HTML', 'NO VALUE', 'Low Risk']],
                                   columns=['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'])
        save_risk_csv('test_data', new_risk_df)

        # Tests the contents of the csv are correct.
        result = csv_to_list(os.path.join('test_data', f"test_data_full_risk_data_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level'],
                    ['Word', 'NO VALUE', 'No Match'],
                    ['PDF/A-1a', 'NO VALUE', 'Low Risk'],
                    ['Rich Text', '1.6', 'Low Risk'],
                    ['HTML', 'NO VALUE', 'Low Risk']]
        self.assertEqual(result, expected, 'Problem with test for duplicates')


if __name__ == '__main__':
    unittest.main()
