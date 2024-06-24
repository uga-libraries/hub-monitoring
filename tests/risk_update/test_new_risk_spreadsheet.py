"""
Test for the function new_risk_spreadsheet() which combines existing format data with new NARA risk data.
"""
import unittest
from risk_update import new_risk_spreadsheet, read_nara_csv
from test_script_risk_update import csv_to_list
from datetime import datetime
from os import remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test outputs if they were created"""
        # List of paths for possible test outputs.
        today = datetime.today().strftime('%Y-%m-%d')
        outputs = [join('test_data', 'Russell_Hub', 'update_risk_log.csv'),
                   join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er', f'2005-10-er_full_risk_data_{today}.csv'),
                   join('test_data', 'Russell_Hub', 'rbrl004', '2021-40-er', f'2021-40-er_full_risk_data_{today}.csv')]

        # Deletes any test output that is present.
        for output in outputs:
            if exists(output):
                remove(output)

    def test_blank_columns(self):
        """Test for when no format has a version or PUID, resulting in blank version and PUID columns"""
        # Creates input variables and runs the function.
        root = join('test_data', 'Russell_Hub', 'rbrl004', '2021-40-er')
        file = '2021-40-er_full_risk_data.csv'
        nara_risk_df = read_nara_csv(join('test_data', 'NARA_PreservationActionPlan.csv'))
        directory = join('test_data', 'Russell_Hub')
        new_risk_spreadsheet(root, file, nara_risk_df, directory)

        # Tests the expected log CSV was made.
        log_path = join('test_data', 'Russell_Hub', 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for blank columns, log CSV was made")

        # Tests the expected risk CSV was made with the correct file name.
        risk_csv_path = join('test_data', 'Russell_Hub', 'rbrl004', '2021-40-er',
                             f"2021-40-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")
        risk_csv_made = exists(risk_csv_path)
        self.assertEqual(risk_csv_made, True, "Problem with test for blank columns, risk CSV was made")

        # Tests the risk CSV has the expected contents.
        result = csv_to_list(risk_csv_path)
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2021-40-er\\2021-40-er_bag\\data\\Document.pdf',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'NO VALUE',
                     'Droid version 6.4', False, '3/4/2024', 26, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'Format Name'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2021-40-er\\2021-40-er_bag\\data\\Document.docx', 'Word',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 14, 'fixity_placeholder',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan',
                     'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for blank columns, risk CSV contents")

    def test_no_blank_columns(self):
        """Test for when at least one format has a version and a PUID"""
        # Creates input variables and runs the function.
        root = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er')
        file = '2005-10-er_full_risk_data.csv'
        nara_risk_df = read_nara_csv(join('test_data', 'NARA_PreservationActionPlan.csv'))
        directory = join('test_data', 'Russell_Hub')
        new_risk_spreadsheet(root, file, nara_risk_df, directory)

        # Tests the expected log CSV was made.
        log_path = join('test_data', 'Russell_Hub', 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for no blank columns, log CSV was made")

        # Tests the expected risk CSV was made with the correct file name.
        risk_csv_path = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er',
                             f"2005-10-er_full_risk_data_{datetime.today().strftime('%Y-%m-%d')}.csv")
        risk_csv_made = exists(risk_csv_path)
        self.assertEqual(risk_csv_made, True, "Problem with test for no blank columns, risk CSV was made")

        # Tests the risk CSV has the expected contents.
        result = csv_to_list(risk_csv_path)
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Text Document.rtf',
                     'Rich Text Format', '1.6', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Droid version 6.4', False, '3/4/2024', 43, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Web Page.html',
                     'HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Droid version 6.4', False, '3/4/2024', 30, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Hypertext Markup Language 5.2', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Web Page.html',
                     'HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Droid version 6.4', False, '3/4/2024', 30, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Document.pdf',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'NO VALUE', 'NO VALUE',
                     'Droid version 6.4', False, '3/4/2024', 26, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'Format Name'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Document.docx', 'Word',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 14, 'fixity_placeholder',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan',
                     'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for no blank columns, risk CSV contents")


if __name__ == '__main__':
    unittest.main()
