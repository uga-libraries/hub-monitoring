"""
Tests for the function validate_bag(), which validates an accession's bag
and returns if it is valid and the error message.
"""
import unittest
from validate_fixity import validate_bag
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
        accessions = [join('test_data', 'test_001_bags_valid', '2023_test001_001_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_001_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_002_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_003_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_004_er'),
                      join('test_data', 'test_002_bags_invalid', '2023_test002_005_er')]
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # Deletes the script report, if made.
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('test_data', f"fixity_validation_{today}.csv")):
            remove(join('test_data', f"fixity_validation_{today}.csv"))

    # def test_bag_error(self):
    #     """Template for test for when the bag cannot be validated because bagit gives a BagError
    #     This is caused by path length and cannot be reliably replicated in the test data.
    #     Instead, supply the path in root and folder to a bag known to have this error.
    #     After the test runs, remove the data from preservation_log.txt and
    #     delete any fixity_validation.csv and manifest_validation_errors.csv produced.
    #     """
    #     # Makes variables for function input and runs the function.
    #     root = r'INSERT PATH TO ACCESSION FOLDER'
    #     folder = 'INSERT NAME OF BAG FOLDER'
    #     validate_bag(join(root, folder), r'INSERT PATH FOR WHERE TO SAVE REPORT')
    #
    #     # Verifies the preservation_log.txt has been updated correctly.
    #     result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
    #     expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
    #                 ['INSERT DATA ROWS']]
    #     self.assertEqual(result, expected, 'Problem with test for bag error, preservation_log.txt')
    #
    #     # Verifies the fixity validation CSV has the correct values.
    #     # Only use for bags that are not valid.
    #     result = csv_to_list(join(r'INSERT PATH FOR WHERE TO SAVE REPORT',
    #                               f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
    #     expected = [['Accession', 'Validation_Error'],
    #                 ['INSERT DATA ROW(s)']]
    #     self.assertEqual(result, expected, 'Problem with test for bag error, fixity_validation.csv')

    def test_file_added(self):
        """Test for when the bag is not valid because a file was added"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er')
        folder = '2023_test002_001_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.1.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for file added, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test002_001_er',
                     'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes']]
        self.assertEqual(result, expected, 'Problem with test for file added, fixity_validation.csv')

    def test_file_deleted(self):
        """Test for when the bag is not valid because a file was deleted"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_002_er')
        folder = '2023_test002_002_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.2.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.2.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.2.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.2.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for file deleted, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test002_002_er',
                     'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes']]
        self.assertEqual(result, expected, 'Problem with test for file deleted, fixity_validation.csv')

    def test_file_edited(self):
        """Test for when the bag is not valid because a file was edited"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_003_er')
        folder = '2023_test002_003_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.3.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.3.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.3.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.3.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.3.ER. The bag is not valid. Payload-Oxum validation failed. '
                     'Expected 3 files and 47 bytes but found 3 files and 79 bytes',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for file edited, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test002_003_er',
                     'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 3 files and 79 bytes']]
        self.assertEqual(result, expected, 'Problem with test for file edited, fixity_validation.csv')

    def test_fixity_changed(self):
        """Test for when the bag is not valid because a file's fixity was changed in the manifest"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_004_er')
        folder = '2023_test002_004_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.4.ER. The bag is not valid. Bag validation failed: '
                     'data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for fixity changed, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test002_004_er',
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"']]
        self.assertEqual(result, expected, 'Problem with test for fixity changed, fixity_validation.csv')

    def test_missing_bag_info(self):
        """Test for when the bag is not valid because bag-info.txt is missing"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_005_er')
        folder = '2023_test002_005_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.5.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.5.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.5.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.5.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.5.ER. The bag is not valid. Bag validation failed: '
                     'bag-info.txt exists in manifest but was not found on filesystem', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for missing bag-info.txt, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test002_005_er',
                     'Bag validation failed: bag-info.txt exists in manifest but was not found on filesystem']]
        self.assertEqual(result, expected, 'Problem with test for missing bag-info.txt, fixity_validation.csv')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_001_bags_valid', '2023_test001_001_er')
        folder = '2023_test001_001_er_bag'
        validate_bag(join(root, folder), 'test_data')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.1.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')

        # Verifies the script report fixity validation CSV was not made.
        result = exists(join('test_data', f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, 'Problem with test for valid, fixity_validation.csv')


if __name__ == '__main__':
    unittest.main()
