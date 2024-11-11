"""
Tests for the script risk_update.py, Get updated NARA risk information for every accession in a input_directory.
"""
import csv
from datetime import date
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = pd.read_csv(csv_path)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Variable calculated several times"""
        self.today = date.today().strftime('%Y-%m-%d')

    def tearDown(self):
        """Delete the test outputs if they were created"""
        # List of paths for possible test outputs.
        new_path = os.path.join('test_data', 'script_new', 'rbrl004')
        restart_path = os.path.join('test_data', 'script_restart')
        outputs = (os.path.join(new_path, '2005-10-er', f'2005-10-er_full_risk_data_{self.today}.csv'),
                   os.path.join(new_path, '2005-20-er', f'2005-20-er_full_risk_data_{self.today}.csv'),
                   os.path.join(new_path, '2006-30-er', f'2006-30-er_full_risk_data_{self.today}.csv'),
                   os.path.join(new_path, '2021-40-er', f'2021-40-er_full_risk_data_{self.today}.csv'),
                   os.path.join(new_path, f'risk_update_log_{self.today}.csv'),
                   os.path.join(restart_path, 'rbrl004', '2006-30-er', f'2006-30-er_full_risk_data_{self.today}.csv'),
                   os.path.join(restart_path, 'rbrl004', '2021-40-er', f'2021-40-er_full_risk_data_{self.today}.csv'),
                   os.path.join(restart_path, f'risk_update_log_{self.today}.csv'))

        # Deletes any test output that is present.
        for output in outputs:
            if os.path.exists(output):
                os.remove(output)

    def test_new(self):
        """Test for when the script runs for the first time (risk update log does not exist)"""
        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'risk_update.py')
        input_directory = os.path.join('test_data', 'script_new', 'rbrl004')
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_FileFormats_20240912.csv')
        subprocess.run(f'python "{script}" "{input_directory}" "{nara_csv}"', shell=True, stdout=subprocess.PIPE)

        # Tests the contents of the risk update log are correct.
        result = csv_to_list(os.path.join(input_directory, f'risk_update_log_{self.today}.csv'))
        expected = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                    ['rbrl004', '2005-10-er', os.path.join(input_directory, '2005-10-er'), 'Yes'],
                    ['rbrl004', '2005-20-er', os.path.join(input_directory, '2005-20-er'), 'Yes'],
                    ['rbrl004', '2006-30-er', os.path.join(input_directory, '2006-30-er'), 'Yes'],
                    ['rbrl004', '2021-40-er', os.path.join(input_directory, '2021-40-er'), 'Yes'],
                    ['rbrl004', '2021-50-er', os.path.join(input_directory, '2021-50-er'), 'No']]
        self.assertEqual(result, expected, "Problem with test for new, risk update log")

        # Tests the contents of 2005-10-er full risk data csv are correct.
        result = csv_to_list(os.path.join(input_directory, '2005-10-er', f'2005-10-er_full_risk_data_{self.today}.csv'))
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
                     'Low Risk', 'Transform to PDF and retain original', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-10-er\\2005-10-er_bag\\data\\Web Page.html',
                     'HYPERTEXT MARKUP LANGUAGE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Droid version 6.4', False, '3/4/2024', 30, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Hypertext Markup Language 5.1', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
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
        self.assertEqual(result, expected, "Problem with test for new, 2005-10-er full risk data csv")

        # Tests the contents of 2005-20-er full risk data csv are correct.
        result = csv_to_list(os.path.join(input_directory, '2005-20-er', f'2005-20-er_full_risk_data_{self.today}.csv'))
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'Portable Document Format (PDF) version 1.0', 'NO VALUE',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Tika version 1.0', True, '3/4/2024', 29,
                     'fixity_placeholder', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain',
                     'PRONOM and Name'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'PDF', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Droid version 6.4',
                     True, '3/4/2024', 29, 'fixity_placeholder', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain', 'PRONOM']]
        self.assertEqual(result, expected, "Problem with test for new, 2005-20-er full risk data csv")

        # Tests the contents of 2006-30-er full risk data csv are correct.
        result = csv_to_list(os.path.join(input_directory, '2006-30-er', f'2006-30-er_full_risk_data_{self.today}.csv'))
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Text Document.rtf',
                     'Rich Text Format', '1.6', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Droid version 6.4', False, '3/4/2024', 41, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Low Risk', 'Transform to PDF and retain original', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 2, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document2.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 4, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for new, 2006-30-er full risk data csv")

        # Tests the contents of 2021-40-er full risk data csv are correct.
        result = csv_to_list(os.path.join(input_directory, '2021-40-er', f'2021-40-er_full_risk_data_{self.today}.csv'))
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
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2021-40-er\\2021-40-er_bag\\data\\Document.rtf', 'Rich Text',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 3, 'fixity_placeholder',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Low Risk',
                     'Transform to PDF and retain original', 'File Extension'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2021-40-er\\2021-40-er_bag\\data\\Document.rtf', 'Rich Text',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 3, 'fixity_placeholder',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Low Risk',
                     'Transform to PDF and retain original', 'File Extension'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2021-40-er\\2021-40-er_bag\\data\\Document.docx', 'Word',
                     'NO VALUE', 'NO VALUE', 'Droid version 6.4', False, '3/4/2024', 14, 'fixity_placeholder',
                     'NO VALUE', 'NO VALUE', 'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan',
                     'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for new, 2021-40-er full risk data csv")

    def test_restart(self):
        """Test for when the script is restarted (risk update log exists)"""
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script_restart')
        
        # Makes the risk update log, with 2 of the 4 accessions already marked as updated.
        # They are not actually updated, so there will not be a new full risk data csv with today's date.
        coll_path = os.path.join(input_directory, 'rbrl004')
        rows = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                ['rbrl004', '2005-10-er', os.path.join(coll_path, '2005-10-er'), 'No'],
                ['rbrl004', '2005-20-er', os.path.join(coll_path, '2005-20-er'), 'Yes'],
                ['rbrl004', '2006-30-er', os.path.join(coll_path, '2006-30-er'), None],
                ['rbrl004', '2021-40-er', os.path.join(coll_path, '2021-40-er'), None]]
        log_path = os.path.join(input_directory, f'risk_update_log_{self.today}.csv')
        with open(log_path, 'w', newline='') as open_log:
            log_writer = csv.writer(open_log)
            log_writer.writerows(rows)

        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'risk_update.py')
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_FileFormats_20240912.csv')
        subprocess.run(f'python "{script}" "{input_directory}" "{nara_csv}"', shell=True, stdout=subprocess.PIPE)

        # Tests the contents of the risk update log are correct.
        result = csv_to_list(os.path.join(input_directory, f'risk_update_log_{self.today}.csv'))
        expected = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                    ['rbrl004', '2005-10-er', os.path.join(coll_path, '2005-10-er'), 'No'],
                    ['rbrl004', '2005-20-er', os.path.join(coll_path, '2005-20-er'), 'Yes'],
                    ['rbrl004', '2006-30-er', os.path.join(coll_path, '2006-30-er'), 'Yes'],
                    ['rbrl004', '2021-40-er', os.path.join(coll_path, '2021-40-er'), 'Yes']]
        self.assertEqual(result, expected, "Problem with test for restart, risk update log")

        # Tests there is not a new full risk data CSV for the accessions already marked as updated.
        result = [os.path.exists(os.path.join(coll_path, '2005-10-er', f'2005-10-er_full_risk_data_{self.today}.csv')),
                  os.path.exists(os.path.join(coll_path, '2005-20-er', f'2005-20-er_full_risk_data_{self.today}.csv'))]
        expected = [False, False]
        self.assertEqual(result, expected, "Problem with test for restart, 2005 full risk data csvs")

        # Tests the contents of 2006-30-er full risk data csv are correct.
        result = csv_to_list(os.path.join(coll_path, '2006-30-er', f'2006-30-er_full_risk_data_{self.today}.csv'))
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Text Document.rtf',
                     'Rich Text Format', '1.6', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Droid version 6.4', False, '3/4/2024', 41, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Low Risk', 'Transform to PDF and retain original', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 2, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document2.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 4, 'fixity_placeholder', 'NO VALUE', 'NO VALUE',
                     'NO VALUE', 'NO VALUE', 'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for restart, 2006-30-er full risk data csv")

        # Tests the contents of 2021-40-er full risk data csv are correct.
        result = csv_to_list(os.path.join(coll_path, '2021-40-er', f'2021-40-er_full_risk_data_{self.today}.csv'))
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
        self.assertEqual(result, expected, "Problem with test for restart, 2021-40-er full risk data csv")

    def test_argument_error(self):
        """Test for when the script arguments are not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = os.path.join(os.getcwd(), '..', '..', 'risk_update.py')
        input_directory = os.path.join('test_data', 'Error', 'closed', 'rbrl004')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{input_directory}"', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct errors.
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Input directory 'test_data\\Error\\closed\\rbrl004' does not exist\r\n" \
                   "Required argument nara_csv is missing\r\n"
        self.assertEqual(result, expected, "Problem with test for argument error, printing")

    def test_nara_csv_error(self):
        """Test for when the column names in the NARA CSV for the columns used are not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = os.path.join(os.getcwd(), '..', '..', 'risk_update.py')
        input_directory = os.path.join('test_data', 'script_new', 'rbrl004')
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_FileFormats_19990125.csv')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{input_directory}" "{nara_csv}"', shell=True, check=True,
                           stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct errors.
        output = subprocess.run(f'python "{script}" "{input_directory}" "{nara_csv}"', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = '\r\nThe NARA Preservation Action Plan spreadsheet does not have at least one of the expected ' \
                   'columns: Format Name, File Extension(s), PRONOM URL, NARA Risk Level, and NARA Proposed ' \
                   'Preservation Plan. The spreadsheet used may be out of date, or NARA may have changed their ' \
                   'spreadsheet organization.\r\n'
        self.assertEqual(result, expected, "Problem with test for nara csv error, printing")


if __name__ == '__main__':
    unittest.main()
