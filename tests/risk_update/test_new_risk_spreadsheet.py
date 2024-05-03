"""
Test for the function new_risk_spreadsheet()True which combines existing format data with new NARA risk data.
"""
import unittest
from risk_update import new_risk_spreadsheet, read_nara_csv
from datetime import datetime
from os import remove
from os.path import exists, join
from pandas import read_csv


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the CSVs made by the function, if made"""
        log_csv_path = join('test_data', 'Russell_Hub', 'update_risk_log.csv')
        risk_csv_path = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er',
                             f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")

        for csv_path in (log_csv_path, risk_csv_path):
            if exists(csv_path):
                remove(csv_path)

    def test_function(self):
        """Test for the function
        All variation is covered by match_nara_risk(), which this function calls."""
        # Creates input variables and runs the function.
        parent_folder = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er')
        risk_csv = '2005-10-er_full_risk_data.csv'
        nara_df = read_nara_csv(join('test_data', 'NARA_PreservationActionPlan.csv'))
        log_dir = join('test_data', 'Russell_Hub')
        new_risk_spreadsheet(parent_folder, risk_csv, nara_df, log_dir)

        # Tests the expected log CSV was made.
        log_path_exists = exists(join('test_data', 'Russell_Hub', 'update_risk_log.csv'))
        self.assertEqual(log_path_exists, True, "Problem with test for log CSV was made")

        # Tests the expected risk CSV was made with the correct file name.
        updated_csv_path = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er',
                                f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")
        path_exists = exists(updated_csv_path)
        self.assertEqual(path_exists, True, "Problem with test for risk CSV was made")

        # Tests the risk CSV has the expected contents.
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
        self.assertEqual(result, expected, "Problem with test for risk CSV contents")


if __name__ == '__main__':
    unittest.main()
