"""
Test for the function new_risk_spreadsheet()True which combines existing format data with new NARA risk data.
"""
import unittest
from risk_update import new_risk_spreadsheet, read_nara_csv
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the CSV made by the function, if it was made"""
        csv_path = join(getcwd(), '..', 'test_data', 'Risk_Update', 'rbrl004', '2005-10-er',
                        f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")
        if exists(csv_path):
            remove(csv_path)

    def test_function(self):
        """Test for the function
        All variation is covered by match_nara_risk(), which this function calls."""
        # Creates input variables and runs the function.
        root = join(getcwd(), '..', 'test_data', 'Risk_Update', 'rbrl004', '2005-10-er')
        file = '2005-10-er_full_risk_data.csv'
        nara_risk_df = read_nara_csv(join(getcwd(), '..', 'test_data', 'NARA_PreservationActionPlan.csv'))
        new_risk_spreadsheet(root, file, nara_risk_df)

        # Tests the expected CSV was made with the correct file name.
        updated_csv_path = join(getcwd(), '..', 'test_data', 'Risk_Update', 'rbrl004', '2005-10-er',
                                f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")
        path_exists = exists(updated_csv_path)
        self.assertEqual(path_exists, True, "Problem with test for CSV was made")

        # Tests the CSV has the expected contents.
        # Replacing blanks with the string "nan" because PyCharm didn't see np.nan as an exact match.
        df = read_csv(updated_csv_path)
        df = df.fillna('nan')
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Text Document.rtf',
                     'Rich Text Format', '1.6', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Droid version 6.4', False, '3/4/2024', 43, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Web Page.html',
                     'HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Droid version 6.4', False, '3/4/2024', 30, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Hypertext Markup Language 5.2', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Web Page.html',
                     'HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Droid version 6.4', False, '3/4/2024', 30, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Document.pdf',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'NO VALUE',
                     'Droid version 6.4', False, '3/4/2024', 26, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'Format Name'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Document.docx', 'Word',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 14, 'fixity_placeholder',
                     'nan', 'nan', 'nan', 'nan', 'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for CSV contents")


if __name__ == '__main__':
    unittest.main()
