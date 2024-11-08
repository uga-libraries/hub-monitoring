"""
Tests for the function read_risk_csv(), which reads the FITs format information columns for a risk CSV into a dataframe.
To simplify testing, all columns are present but the data is abbreviated.
"""
import os
import unittest
from risk_update import read_risk_csv


class MyTestCase(unittest.TestCase):

    def test_blanks(self):
        """Test for when the risk csv includes blank cells"""
        # Creates input variables and runs the function.
        root = os.path.join('test_data', 'read_risk_csv')
        risk_csv_filename = '2006-30-er_full_risk_data_2009-04-01.csv'
        new_risk_df = read_risk_csv(os.path.join(root, risk_csv_filename))

        # Tests the contents of new_risk_df are correct.
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message'],
                    ['Z:\\Doc.txt', 'Plain text', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'FALSE', '3/4/2024', 'NO VALUE',
                     'md51', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE'],
                    ['Z:\\Doc2.txt', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Droid', 'FALSE', 'NO VALUE', '4', 'md52',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE'],
                    ['Z:\\Doc.rtf', 'Rich Text Format', '1.6', 'fmt/50', 'Droid', 'NO VALUE', '3/4/2024', '41',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE']]
        self.assertEqual(result, expected, "Problem with test for blanks")

    def test_no_blanks(self):
        """Test for when the risk csv does not include blank cells"""
        # Creates input variables and runs the function.
        root = os.path.join('test_data', 'read_risk_csv')
        risk_csv_filename = '2021-40-er_full_risk_data.csv'
        new_risk_df = read_risk_csv(os.path.join(root, risk_csv_filename))

        # Tests the contents of new_risk_df are correct.
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message'],
                    ['Z:\\Doc.pdf', 'PDF/A', '1', 'fmt/95', 'Droid', 'FALSE', '3/4/2024', '26', 'md5', 'Adobe',
                     'False', 'False', 'note']]
        self.assertEqual(result, expected, "Problem with test for no blanks")


if __name__ == '__main__':
    unittest.main()
