"""
Tests for the script risk_update.py, Get updated NARA risk information for every accession in a directory.
"""
import subprocess
import unittest
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv


def csv_to_list(csv_path):
    """Make a list of the contents of a CSV, with one list per row, including the header
    Blanks are replaced by the string "nan".
    """
    df = read_csv(csv_path)
    df = df.fillna('nan')
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete script output, if created"""
        today = datetime.today().strftime('%Y-%m-%d')
        coll_folder = join('test_data', 'Russell_Hub', 'rbrl004')
        reports = (join(coll_folder, '2005-10-er', f'2005-10-er_full_risk_data_{today}.csv'),
                   join(coll_folder, '2005-20-er', f'2005-20-er_full_risk_data_{today}.csv'),
                   join(coll_folder, '2006-30-er', f'2006-30-er_full_risk_data_{today}.csv'),
                   join(coll_folder, 'update_risk_log.csv'))
        for report in reports:
            if exists(report):
                remove(report)

    def test_correct(self):
        """Test for when the script runs correctly on all three accessions in rbrl004"""
        # makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'risk_update.py')
        directory = join('test_data', 'Russell_Hub', 'rbrl004')
        nara_csv = join('test_data', 'NARA_PreservationActionPlan.csv')
        subprocess.run(f'python {script} {directory} {nara_csv}', shell=True)

        # Tests the log was made.
        log_path = join('test_data', 'Russell_Hub', 'rbrl004', 'update_risk_log.csv')
        log_path_exists = exists(log_path)
        self.assertEqual(log_path_exists, True, 'Problem with test for log was made')

        # Tests the contents of the log are correct.
        result = csv_to_list(log_path)
        expected = [['Collection', 'Accession'],
                    ['rbrl004', '2005-10-er'],
                    ['rbrl004', '2005-20-er'],
                    ['rbrl004', '2006-30-er']]
        self.assertEqual(result, expected, 'Problem with test for log contents')

        # Paths to the three risk CSVs that should have been made.
        today = datetime.today().strftime('%Y-%m-%d')
        coll_folder = join('test_data', 'Russell_Hub', 'rbrl004')
        csv_paths = [join(coll_folder, '2005-10-er', f'2005-10-er_full_risk_data_{today}.csv'),
                     join(coll_folder, '2005-20-er', f'2005-20-er_full_risk_data_{today}.csv'),
                     join(coll_folder, '2006-30-er', f'2006-30-er_full_risk_data_{today}.csv')]

        # Tests all three risk CSVs were made and have the correct file names.
        paths_exist = []
        for csv_path in csv_paths:
            paths_exist.append(exists(csv_path))
        self.assertEqual(paths_exist, [True, True, True], 'Problem with test for risk CSVs were made')

        # Tests the contents of accession 2005-10-er CSV are correct.
        result = csv_to_list(csv_paths[0])
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
        self.assertEqual(result, expected, 'Problem with test for risk CSV contents, 2005-10-er')

        # Tests the contents of accession 2005-20-er CSV are correct.
        result = csv_to_list(csv_paths[1])
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'Portable Document Format (PDF) version 1.0', 'NO VALUE',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Tika version 1.0', True, '3/4/2024', 29,
                     'fixity_placeholder', 'nan', 'nan', 'nan', 'nan', 'Portable Document Format (PDF) version 1.0',
                     'pdf', 'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain',
                     'PRONOM and Name'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2005-20-er\\2005-20-er_bag\\data\\Folder\\Document.pdf',
                     'PDF', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Droid version 6.4',
                     True, '3/4/2024', 29, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain', 'PRONOM']]
        self.assertEqual(result, expected, 'Problem with test for risk CSV contents, 2005-20-er')

        # Tests the contents of accession 2006-30-er CSV are correct.
        result = csv_to_list(csv_paths[2])
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Text Document.rtf',
                     'Rich Text Format', '1.6', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Droid version 6.4', False, '3/4/2024', 41, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 2, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match'],
                    ['Z:\\Russell_Hub\\backlog\\rbrl004\\2006-30-er\\2006-30-er_bag\\data\\Plain Text Document2.txt',
                     'Plain text', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4', False, '3/4/2024', 4, 'fixity_placeholder', 'nan', 'nan', 'nan', 'nan',
                     'No Match', 'nan', 'nan', 'No Match', 'nan', 'No NARA Match']]
        self.assertEqual(result, expected, 'Problem with test for risk CSV contents, 2006-30-er')

    def test_error(self):
        """Test for when the script arguments are not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'risk_update.py')
        directory = join('test_data', 'Error', 'closed', 'rbrl004')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python {script} {directory}', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct errors.
        output = subprocess.run(f'python {script} {directory}', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Directory 'test_data\\Error\\closed\\rbrl004' does not exist\r\n" \
                   "Required argument nara_csv is missing\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")


if __name__ == '__main__':
    unittest.main()
