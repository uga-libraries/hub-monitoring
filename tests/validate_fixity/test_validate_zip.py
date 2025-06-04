"""
Tests for the function validate_zip(), which validates a zipped accession using an MD5 from a text file.
Updates the preservation log, and if there are errors updates the script report and makes a manifest log.

The test data is not organized into the usual status folders, so status will be "test_data".
"""
from datetime import date
import os
import shutil
import unittest
from validate_fixity import validate_zip
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        and delete the fixity validation log, if made."""
        # Replaces the updated preservation logs for these accessions with a copy of the original logs.
        accessions = [os.path.join('test_data', 'validate_zip', '2023-001-er'),
                      os.path.join('test_data', 'validate_zip', '2023-002-er')]
        for accession in accessions:
            shutil.copyfile(os.path.join(accession, 'preservation_log_copy.txt'),
                            os.path.join(accession, 'preservation_log.txt'))

        # Deletes the fixity validation log report, if made.
        log_path = os.path.join('test_data', f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_not_valid(self):
        """Test for when the accession zip MD5 has changed"""
        # Makes the variables for the function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_manifest', '2023-001-er')
        manifest_name = 'initialmanifest_20231031.csv'
        input_directory = 'test_data'
        result = validate_zip(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Unable to identify folder to validate with the manifest'
        self.assertEqual(result, expected, 'Problem with test for not accession')

    def test_valid(self):
        """Test for when the accession zip MD5 is still the same"""
        # Makes the variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_manifest', '2023-002-er')
        manifest_name = 'initialmanifest_20231003.csv'
        input_directory = 'test_data'
        result = validate_zip(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(os.path.join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.01.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T4.01.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join(input_directory, '2023_test004_001_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid, manifest_validation_errors.csv')

    def test_valid_duplicate(self):
        """Test for when the accession matches the manifest. It includes duplicate files."""
        # Makes the variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_manifest', '2023_test004_002_er')
        manifest_name = 'initialmanifest_20231124.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid + dups, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(os.path.join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.02.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T4.02.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid + dups, preservation_log.txt')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join(input_directory, '2023_test004_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + dups, manifest_validation_errors.csv')

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_manifest', '2023_test004_003_er')
        manifest_name = 'initialmanifest_20240426.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid + FITS, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(os.path.join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.03.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T4.03.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid + FITS, preservation_log.txt')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join(input_directory, '2023_test004_003_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + FITS, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
