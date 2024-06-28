"""
Tests for the function validate_bag_manifest(), which validates an accession using the bag manifest
if bagit cannot do the validation, updates the preservation log,
and if there are errors updates the script report and makes a manifest log.

These tests use bags that would not cause a bagit error, since that is not reliably replicable.
This function does not depend on the error, so it can use a normal bag.

The test data is not organized into the usual status folders, so status will be "test_data".
"""
import unittest
from validate_fixity import validate_bag_manifest
from test_script_validate_fixity import csv_to_list
from datetime import date
from os import remove
from os.path import exists, join
from shutil import copyfile


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        and delete other function outputs."""
        # Replaces the updated preservation logs for these accessions with a copy of the original logs.
        accessions = [join('test_data', 'test_001_bags_valid', '2023_test001_002_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_001_er')]
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # Deletes the script report, if made.
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('test_data', f"fixity_validation_{today}.csv")):
            remove(join('test_data', f"fixity_validation_{today}.csv"))

        # Deletes the manifest log, if made.
        if exists(join('test_data', '2023_test002_001_er_manifest_validation_errors.csv')):
            remove(join('test_data', '2023_test002_001_er_manifest_validation_errors.csv'))

    def test_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        bag_dir = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', '2023_test002_001_er_bag')
        validate_bag_manifest(bag_dir, 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', 'preservation_log.txt'),
                             delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag manifest for accession 2023.2.1.ER. The bag manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Validation_Error'],
                    ['test_data', 'test_002_bags_invalid', '2023_test002_001_er', '1 bag manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join('test_data', '2023_test002_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', '2023_test002_001_er_bag',
                          'data', 'CD_2', 'New Text Document.txt'), '0ee0d2e5ec9772cce389da723946d788', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid, manifest_validation_errors.csv')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes the variable needed for function input and runs the function.
        bag_dir = join('test_data', 'test_001_bags_valid', '2023_test001_002_er', '2023_test001_002_er_bag')
        validate_bag_manifest(bag_dir, 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join('test_data', 'test_001_bags_valid', '2023_test001_002_er', 'preservation_log.txt'),
                             delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag manifest for accession 2023.1.2.ER. The bag manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')

        # Verifies the fixity validation CSV was not made.
        result = exists(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, 'Problem with test for valid, fixity_validation.csv')

        # Verifies the manifest log was not made.
        result = exists(join('test_data', '2023_test001_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
