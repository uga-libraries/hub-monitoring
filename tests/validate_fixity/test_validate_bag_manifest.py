"""
Start for tests for the function validate_bag_manifest(), which validates an accession using the bag manifest
if bagit cannot do the validation.

These tests use bags that would not cause a bagit error, since that is not reliably replicable.
This function does not depend on the error, so it can use a normal bag.
"""
import unittest
from validate_fixity import validate_bag_manifest
from test_script_validate_fixity import csv_to_list
from datetime import date
from os.path import join
from shutil import copyfile


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder"""
        # List of paths for accessions with logs to replace.
        accessions = [join('test_data', 'test_001_bags_valid', '2023_test001_002_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_001_er')]

        # For each accession, replaces the updated log with a copy of the original log from the accession folder.
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

    def test_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variable needed for function input and runs the function.
        bag_dir = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', '2023_test002_001_er_bag')
        validate_bag_manifest(bag_dir)

        # Verifies the contents of the preservation_log.txt have been updated.
        result = csv_to_list(join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.001',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.001',
                     'Bagged with accession 2023.test002.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.002',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.002',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'CD.002',
                     'Bagged with accession 2023.test002.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', '2023-01-31', 'nan',
                     'Validated bag for accession 2023.test002.001.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.002', '2023.test002.001.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test002.001.ER. The bag is not valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid, preservation_log.txt')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes the variable needed for function input and runs the function.
        bag_dir = join('test_data', 'test_001_bags_valid', '2023_test001_002_er', '2023_test001_002_er_bag')
        validate_bag_manifest(bag_dir)

        # Verifies the contents of the preservation_log.txt have been updated.
        result = csv_to_list(join('test_data', 'test_001_bags_valid', '2023_test001_002_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001',
                     'Bagged with accession 2023.test001.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002',
                     'Bagged with accession 2023.test001.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'nan',
                     'Validated bag for accession 2023.test001.002.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test001.002.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')


if __name__ == '__main__':
    unittest.main()
