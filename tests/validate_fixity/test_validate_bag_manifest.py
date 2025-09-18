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
        for accession in ['2023_test002_001_er', '2023_test003_011_er']:
            manifest = f'{accession}_manifest_validation_errors.csv'
            if os.path.exists(os.path.join('test_data', manifest)):
                os.remove(os.path.join('test_data', manifest))

    def test_not_valid_bag(self):
        """Test for when the bag is not valid and uses the acc_bag naming convention"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test002_001_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir, '2023_test002_001_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Could not validate with bagit. Bag manifest not valid: 1 errors'
        self.assertEqual(result, expected, 'Problem with test for not valid bag, validation_result')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(os.path.join('test_data', '2023_test002_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [os.path.join(acc_dir, '2023_test002_001_er_bag', 'data', 'CD_2', 'New Text Document.txt'),
                     '0ee0d2e5ec9772cce389da723946d788', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid bag, manifest')

    def test_not_valid_zipped_bag(self):
        """Test for when the bag is not valid and uses the acc_zipped_bag naming convention"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test003_011_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir, '2023_test003_011_er_zipped_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Could not validate with bagit. Bag manifest not valid: 4 errors'
        self.assertEqual(result, expected, 'Problem with test for not valid zipped bag, validation_result')

        # Verifies the manifest log has the correct values.
        data_path = os.path.join(acc_dir, '2023_test003_011_er_zipped_bag', 'data')
        result = csv_to_list(os.path.join('test_data', '2023_test003_011_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['data.zip', '9aaf11684f3f9c075ea71946f331f075', 'Manifest'],
                    [os.path.join(data_path, 'data.zip'), '7a781f9ad56aafd228607f20c90adfc2', 'Current'],
                    [os.path.join(data_path, 'new_file.txt'), '9ecc761c0dd665a119ca11c963b28e43', 'Current'],
                    [os.path.join(data_path, 'new_file_2.txt'), '9ecc761c0dd665a119ca11c963b28e43', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid zipped bag, manifest')

    def test_valid_bag(self):
        """Test for when the bag is valid and uses the acc_bag naming convention"""
        # Makes the variable needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test001_002_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir, '2023_test001_002_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Valid (bag manifest - could not validate with bagit)'
        self.assertEqual(result, expected, 'Problem with test for valid bag, validation_result')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join('test_data', '2023_test001_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid bag, manifest_validation_errors.csv')

    def test_valid_zipped_bag(self):
        """Test for when the bag is valid and uses the acc_zipped_bag naming convention"""
        # Makes the variable needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'validate_bag_manifest', '2023_test003_010_er')
        report_dir = 'test_data'
        result = validate_bag_manifest(acc_dir, report_dir, '2023_test003_010_er_zipped_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Valid (bag manifest - could not validate with bagit)'
        self.assertEqual(result, expected, 'Problem with test for valid zipped bag, validation_result')

        # Verifies the manifest log was not made.
        result = os.path.exists(os.path.join('test_data', '2023_test003_010_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid zipped bag, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
