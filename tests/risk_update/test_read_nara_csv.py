"""
Tests for the function read_nara_csv(), which reads the NARA CSV and renames columns used in the script output.
"""
import os
import unittest
from risk_update import read_nara_csv


class MyTestCase(unittest.TestCase):

    def test_current_nara(self):
        """Test for when the column names in the NARA CSV for the 5 columns used are correct, as of June 2024"""
        # Creates input variable (in production, this is a script argument) and runs the function.
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan.csv')
        nara_risk_df = read_nara_csv(nara_csv)

        # Tests the contents of nara_risk_df is correct.
        df = nara_risk_df.fillna('nan')
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [['NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan'],
                    ['Hypertext Markup Language 5.2', 'htm|html', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain'],
                    ['Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain'],
                    ['Portable Document Format (PDF) Portfolio 2.0', 'pdf', 'nan', 'Moderate Risk',
                     'Retain but possibly extract files from the container'],
                    ['Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain'],
                    ['Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain'],
                    ['Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF'],
                    ['Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF'],
                    ['WordPerfect Template', 'wpt', 'nan', 'Moderate Risk', 'Transform to PDF if possible']]
        self.assertEqual(result, expected)

    def test_incorrect_nara(self):
        """Test for when the column names in the NARA CSV for the 5 columns used are not correct"""
        # Creates input variable (in production, this is a script argument).
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_Outdated.csv')

        # Runs the function and verifies it raises the expected error.
        with self.assertRaises(KeyError):
            read_nara_csv(nara_csv)


if __name__ == '__main__':
    unittest.main()
