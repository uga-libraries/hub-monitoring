"""
Test for the function read_risk_csv(), which reads the FITs format information columns for a risk CSV into a dataframe.
"""
import unittest
from risk_update import read_risk_csv
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for the function, which has no variations"""
        # Creates input variables and runs the function.
        root = join('test_data', 'script', 'rbrl004', '2005-20-er')
        file = '2005-20-er_full_risk_data_2012-07-01.csv'
        new_risk_df = read_risk_csv(join(root, file))

        # Tests the contents of new_risk_df are correct.
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'PDF', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Droid version 6.4',
                     'TRUE', '3/4/2024', '29', 'fixity_placeholder', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'Portable Document Format (PDF) version 1.0', 'NO VALUE',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Tika version 1.0', 'TRUE', '3/4/2024',
                     '29', 'fixity_placeholder', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE']]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
