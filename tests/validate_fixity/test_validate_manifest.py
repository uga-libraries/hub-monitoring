"""
Tests for the function validate_manifest(), which validates an accession using a manifest, updates the preservation log,
and if there are errors updates the script report and makes a manifest log.

The test data is not organized into the usual status folders, so status will be "test_data".
"""
import unittest
from validate_fixity import validate_manifest
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
        accessions = [join('test_data', 'validate_manifest', '2023_test004_001_er'),
                      join('test_data', 'validate_manifest', '2023_test004_002_er'),
                      join('test_data', 'validate_manifest', '2023_test004_003_er'),
                      join('test_data', 'validate_manifest', '2023_test005_001_er'),
                      join('test_data', 'validate_manifest', '2023_test005_002_er'),
                      join('test_data', 'validate_manifest', '2023_test005_003_er'),
                      join('test_data', 'validate_manifest', '2023_test005_004_er'),
                      join('test_data', 'validate_manifest', '2023_test005_005_er')]
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # Deletes the script report, if made.
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('test_data', f"fixity_validation_log_{today}.csv")):
            remove(join('test_data', f"fixity_validation_log_{today}.csv"))

        # Deletes the manifest log, if made.
        for acc_num in range(1, 6):
            if exists(join('test_data', f'2023_test005_00{str(acc_num)}_er_manifest_validation_errors.csv')):
                remove(join('test_data', f'2023_test005_00{str(acc_num)}_er_manifest_validation_errors.csv'))

    # def test_file_not_found(self):
    #     """Use this as a template to test against an accession known to have the error,
    #     which is from file path length and cannot be replicated in the repo test data.
    #     The test will alter the preservation log, so either make a copy first to revert to after the test
    #     or edit the preservation log to remove the test outputs. Also delete the script report and manifest log.
    #     """
    #     accession_path = 'INSERT-PATH-TO-ACCESSION'
    #     manifest_name = 'initialmanifest_INSERT-DATE.csv'
    #     input_directory = 'INSERT-PATH-TO-SAVE-SCRIPT-OUTPUT'
    #     validate_manifest(accession_path, manifest_name, input_directory)
    #     # Test will always pass. Look at the results to determine if it worked correctly,
    #     # or use the other tests below to set up tests of the logs with expected values.
    #     self.assertEqual(True, True)

    def test_not_accession(self):
        """Test for when an initialmanifest.csv is in a folder that does not contain any folders,
        so the script cannot validate it. This happens when something is not organized as expected."""
        # Makes the variables for the function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_006_er')
        manifest_name = 'initialmanifest_20231031.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Unable to identify folder to validate with the manifest'
        self.assertEqual(result, expected, 'Problem with test for not accession')

    def test_not_valid_deletion(self):
        """Test for when the accession does not match the manifest due to file deletions."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_001_er')
        manifest_name = 'initialmanifest_20230501.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = '2 manifest errors'
        self.assertEqual(result, expected, 'Problem with test for not valid/del, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.01.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T5.01.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del, preservation_log.txt')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(input_directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 2 in the manifest.',
                     'BLANK', 'BLANK']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del, manifest_validation_errors.csv')

    def test_not_valid_deletion_all_duplicates(self):
        """Test for when the accession does not match the manifest due to file deletions.
        All copies of a duplicate file have been deleted."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_003_er')
        manifest_name = 'initialmanifest_20230511.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = '3 manifest errors'
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.03.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T5.03.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, preservation_log.txt')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(input_directory, '2023_test005_003_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_003_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    ['Z:\\2023_test005_003_er\\CD_2\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 3 in the manifest.',
                     'BLANK', 'BLANK']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, manifest_validation_errors.csv')

    def test_not_valid_deletion_some_duplicates(self):
        """Test for when the accession matches the manifest due to only some duplicate files being deleted.
        Change is detected based on the number of files, not fixity.
        """
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_005_er')
        manifest_name = 'initialmanifest_20231031.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = '1 manifest errors'
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.05.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T5.05.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, preservation_log.txt')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(input_directory, '2023_test005_005_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Number of files does not match. 2 files in the accession folder and 4 in the manifest.',
                     'BLANK', 'BLANK']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, manifest_validation_errors.csv')

    def test_not_valid_edit(self):
        """Test for when the accession does not match the manifest due to files being edited."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_002_er')
        manifest_name = 'initialmanifest_20230601.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = '4 manifest errors'
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.02.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T5.02.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, preservation_log.txt')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(input_directory, '2023_test005_002_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(accession_path, '2023_test005_002_er', 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E',
                     'Current'],
                    [join(accession_path, '2023_test005_002_er', 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30',
                     'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, manifest_validation_errors.csv')

    def test_not_valid_edit_duplicates(self):
        """Test for when the accession does not match the manifest due to files being edited.
        The edited file was one of three copies. The other two copies were not edited."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test005_004_er')
        manifest_name = 'initialmanifest_20230521.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = '1 manifest errors'
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'BLANK', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'BLANK', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.04.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated manifest for accession 2023.T5.04.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, preservation_log.txt')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(input_directory, '2023_test005_004_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [join(accession_path, '2023_test005_004_er', 'CD_2', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E',
                     'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, manifest_validation_errors.csv')

    def test_valid(self):
        """Test for when the accession matches the manifest."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test004_001_er')
        manifest_name = 'initialmanifest_20231003.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
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
        result = exists(join(input_directory, '2023_test004_001_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid, manifest_validation_errors.csv')

    def test_valid_duplicate(self):
        """Test for when the accession matches the manifest. It includes duplicate files."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test004_002_er')
        manifest_name = 'initialmanifest_20231124.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid + dups, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
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
        result = exists(join(input_directory, '2023_test004_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + dups, manifest_validation_errors.csv')

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        accession_path = join('test_data', 'validate_manifest', '2023_test004_003_er')
        manifest_name = 'initialmanifest_20240426.csv'
        input_directory = 'test_data'
        result = validate_manifest(accession_path, manifest_name, input_directory)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid + FITS, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(accession_path, 'preservation_log.txt'), delimiter='\t')
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
        result = exists(join(input_directory, '2023_test004_003_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + FITS, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
