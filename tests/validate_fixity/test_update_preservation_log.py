"""
Tests for the function update_preservation_log(), which adds validation information to an accession's preservation log.
"""
import unittest
from validate_fixity import update_preservation_log
from test_script_validate_fixity import csv_to_list
from datetime import date
from os.path import join
from shutil import copyfile


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder"""
        # List of paths for accessions with logs to replace.
        accessions = [join('test_data', 'test_003_log_update', '2023_test003_001_er'),
                      join('test_data', 'test_003_log_update', '2023_test003_002_er'),
                      join('test_data', 'test_003_log_update', '2023_test003_005_er'),
                      join('test_data', 'test_003_log_update', '2023_test003_006_er')]

        # For each accession, replaces the updated log with a copy of the original log from the accession folder.
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

    def test_bag_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        accession_directory = join('test_data', 'test_003_log_update', '2023_test003_001_er')
        error = 'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes'
        update_preservation_log(accession_directory, False, 'bag', error)

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(accession_directory, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'nan', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.1.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for bag, not valid')

    def test_bag_valid(self):
        """Test for when the bag is valid"""
        # Makes the variables needed for function input and runs the function.
        accession_directory = join('test_data', 'test_003_log_update', '2023_test003_002_er')
        update_preservation_log(accession_directory, True, 'bag')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(accession_directory, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'nan', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for bag, valid')

    def test_manifest_not_valid(self):
        """Test for when the manifest is not valid"""
        # Makes the variables needed for function input and runs the function.
        accession_directory = join('test_data', 'test_003_log_update', '2023_test003_005_er')
        update_preservation_log(accession_directory, False, 'manifest')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(accession_directory, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.5.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.5.ER', '2023-02-28', 'nan', 'Made manifest, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.5.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.5.ER. The manifest is not valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for manifest, not valid')

    def test_manifest_valid(self):
        """Test for when the manifest is valid"""
        # Makes the variables needed for function input and runs the function.
        accession_directory = join('test_data', 'test_003_log_update', '2023_test003_006_er')
        update_preservation_log(accession_directory, True, 'manifest')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(accession_directory, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.6.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.6.ER', '2023-02-28', 'nan', 'Made manifest, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.6.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.6.ER. The manifest is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for manifest, valid')

    # def test_no_log(self):
    #     """Test for when there is no preservation log to update
    #     Haven't figured out how to test what a function prints automatically,
    #     so this will cause the function to print to the terminal when the test runs.
    #     """
    #     # Makes the variables needed for function input and runs the function.
    #     accession_directory = join('test_data', 'test_003_log_update', '2023_test003_007_er')
    #     update_preservation_log(accession_directory, True, 'manifest')
    #     self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
