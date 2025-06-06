"""
Tests for the function validate_bag_manifest(), which validates an accession using the bag manifest
if bagit cannot do the validation, if there are errors makes a manifest log, and returns information for the logs..

These tests use bags that would not cause a bagit error, since that is not reliably replicable.
This function does not depend on the error, so it can use a normal bag.
"""
import os
import unittest
from validate_fixity import validate_bag_manifest
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the manifest validation errors csv, if made."""
        if os.path.exists(os.path.join('test_data', '2023_test002_001_er_manifest_validation_errors.csv')):
            os.remove(os.path.join('test_data', '2023_test002_001_er_manifest_validation_errors.csv'))

    def test_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test002_001_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir)

        # Verifies the function returned the correct validation_result.
        expected = 'Could not validate with bagit. Bag manifest not valid: 1 errors'
        self.assertEqual(result, expected, 'Problem with test for not valid, validation_result')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(os.path.join('test_data', '2023_test002_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [os.path.join(acc_dir, f'{os.path.basename(acc_dir)}_bag', 'data', 'CD_2', 'New Text Document.txt'),
                     '0ee0d2e5ec9772cce389da723946d788', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid, manifest_validation_errors.csv')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes the variable needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test001_002_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid (bag manifest - could not validate with bagit)'
        self.assertEqual(result, expected, 'Problem with test for not valid, validation_result')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join('test_data', '2023_test001_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
