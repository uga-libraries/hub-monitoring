"""
Test for the function read_nara_csv(), which reads the NARA CSV and renames columns used in the script output.
"""
import unittest
from risk_update import read_nara_csv
from numpy import nan
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for the function
        There is no input variation or error handling.
        The script verifies the path to the CSV is valid before this function runs."""
        # Creates input variable (in production, this is a script argument) and runs the function.
        nara_csv = join(getcwd(), '..', 'test_data', 'NARA_PreservationActionPlan.csv')
        nara_risk_df = read_nara_csv(nara_csv)

        # Tests the contents of nara_risk_df is correct.
        result = [nara_risk_df.columns.tolist()] + nara_risk_df.values.tolist()
        expected = [['NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan'],
                    ['Hypertext Markup Language 5.2', 'htm|html', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain'],
                    ['Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain'],
                    ['Portable Document Format (PDF) Portfolio 2.0', 'pdf', nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container'],
                    ['Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain'],
                    ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain'],
                    ['Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF'],
                    ['Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF'],
                    ['WordPerfect Template', 'wpt', nan, 'Moderate Risk', 'Transform to PDF if possible']]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
