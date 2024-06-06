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
        accessions = [join('test_data', 'test_006_log_update', '2023_test006_001_er'),
                      join('test_data', 'test_006_log_update', '2023_test006_002_er'),
                      join('test_data', 'test_006_log_update', '2023_test006_003_er'),
                      join('test_data', 'test_006_log_update', '2023_test006_004_er'),
                      join('test_data', 'test_006_log_update', '2023_test006_006_er'),
                      join('test_data', 'test_006_log_update', '2023_test006_007_er')]

        # For each accession, replaces the updated log with a copy of the original log from the accession folder.
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

    def test_bag_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        root = join('test_data', 'test_006_log_update', '2023_test006_001_er')
        is_valid = False
        error = 'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes'
        update_preservation_log(root, is_valid, 'bag', error)

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'nan', 'Validated bag for accession. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.1.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for bag, not valid')

    def test_bag_valid(self):
        """Test for when the bag is valid"""
        # Makes the variables needed for function input and runs the function.
        root = join('test_data', 'test_006_log_update', '2023_test006_002_er')
        is_valid = True
        error = None
        update_preservation_log(root, is_valid, 'bag', error)

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'nan', 'Validated bag for accession. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for bag, valid')

    def test_manifest_not_valid(self):
        """Test for when the manifest is not valid"""
        # Makes the variables needed for function input and runs the function.
        root = join('test_data', 'test_006_log_update', '2023_test006_003_er')
        is_valid = False
        update_preservation_log(root, is_valid, 'manifest')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'nan', 'Cannot bag. Made manifest. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.3.ER. The manifest is not valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for manifest, not valid')

    def test_manifest_valid(self):
        """Test for when the manifest is valid"""
        # Makes the variables needed for function input and runs the function.
        root = join('test_data', 'test_006_log_update', '2023_test006_004_er')
        is_valid = True
        update_preservation_log(root, is_valid, 'manifest')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'nan', 'Cannot bag. Made manifest. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.4.ER. The manifest is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for manifest, valid')


if __name__ == '__main__':
    unittest.main()
