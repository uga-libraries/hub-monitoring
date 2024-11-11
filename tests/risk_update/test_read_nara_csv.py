"""
Tests for the function read_nara_csv(), which reads the NARA CSV and renames columns used in the script output.
"""
import os
import unittest
from risk_update import read_nara_csv
from test_read_risk_csv import df_to_list


class MyTestCase(unittest.TestCase):

    def test_current_nara(self):
        """Test for when the column names in the NARA CSV for the 5 columns used are correct, as of June 2024"""
        # Creates input variable (in production, this is a script argument) and runs the function.
        # This spreadsheet has all the NARA columns but only 8 rows of data.
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_FileFormats_20240325.csv')
        nara_risk_df = read_nara_csv(nara_csv)

        # Tests the contents of nara_risk_df is correct.
        result = df_to_list(nara_risk_df)
        expected = [['NARA_Format_Name', 'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level',
                     'NARA_Proposed_Preservation_Plan'],
                    ['Graphics Interchange Format 87a', 'gif', 'https://www.nationalarchives.gov.uk/pronom/fmt/3',
                     'Moderate Risk', 'Retain'],
                    ['Graphics Interchange Format 89a', 'gif', 'https://www.nationalarchives.gov.uk/pronom/fmt/4',
                     'Low Risk', 'Retain'],
                    ['Graphics Interchange Format unspecified version', 'gif', 'nan', 'Moderate Risk', 'Retain'],
                    ['GZIP', 'gz|tgz', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/266', 'Moderate Risk',
                     'Retain but extract files from the container'],
                    ['JPEG 2000 File Format', 'jp2|jpx', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/392',
                     'Low Risk', 'Retain'],
                    ['JPEG File Interchange Format 1.00', 'jpg|jpeg|jpe',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/42', 'Low Risk', 'Retain'],
                    ['JPEG File Interchange Format 1.01', 'jpg|jpeg|jpe',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Low Risk', 'Retain'],
                    ['JPEG File Interchange Format 1.02', 'jpg|jpeg|jpe',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/44', 'Low Risk', 'Retain']]
        self.assertEqual(result, expected, "Problem with test for current NARA")

    def test_incorrect_nara(self):
        """Test for when the column names in the NARA CSV for the 5 columns used are not correct"""
        # Creates input variable (in production, this is a script argument).
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan_FileFormats_19990125.csv')

        # Runs the function and verifies it raises the expected error.
        with self.assertRaises(KeyError):
            read_nara_csv(nara_csv)


if __name__ == '__main__':
    unittest.main()
