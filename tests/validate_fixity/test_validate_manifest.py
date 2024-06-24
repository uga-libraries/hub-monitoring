"""
Tests for the function validate_manifest(), which validates an accession using a manifest, updates the preservation log,
and if there are errors updates the script report and makes a manifest log.
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
        accessions = [join('test_data', 'test_004_manifest_valid', '2023_test004_001_er'),
                      join('test_data', 'test_004_manifest_valid', '2023_test004_002_er'),
                      join('test_data', 'test_004_manifest_valid', '2023_test004_003_er'),
                      join('test_data', 'test_005_manifest_not_valid', '2023_test005_001_er'),
                      join('test_data', 'test_005_manifest_not_valid', '2023_test005_002_er'),
                      join('test_data', 'test_005_manifest_not_valid', '2023_test005_003_er'),
                      join('test_data', 'test_005_manifest_not_valid', '2023_test005_004_er'),
                      join('test_data', 'test_005_manifest_not_valid', '2023_test005_005_er')]
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # Deletes the script report, if made.
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('test_data', f"fixity_validation_{today}.csv")):
            remove(join('test_data', f"fixity_validation_{today}.csv"))

        # Deletes the manifest log, if made.
        for acc_num in range(1, 6):
            if exists(join('test_data', f'2023_test005_00{str(acc_num)}_er_manifest_validation_errors.csv')):
                remove(join('test_data', f'2023_test005_00{str(acc_num)}_er_manifest_validation_errors.csv'))

    def test_filenotfound_attempt(self):
        """Trying to replicate file not found error"""
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_006_er')
        file = 'initialmanifest_20231031.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)
        self.assertEqual(True, True)

    def test_not_valid_deletion(self):
        """Test for when the accession does not match the manifest due to file deletions."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_001_er')
        file = 'initialmanifest_20230501.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.01.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.01.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.01.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test005_001_er', '2 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 2 in the manifest.',
                     'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del, manifest_validation_errors.csv')

    def test_not_valid_deletion_all_duplicates(self):
        """Test for when the accession does not match the manifest due to file deletions.
        All copies of a duplicate file have been deleted."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_003_er')
        file = 'initialmanifest_20230511.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.03.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.03.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.03.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test005_003_er', '3 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(directory, '2023_test005_003_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_003_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    ['Z:\\2023_test005_003_er\\CD_2\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 3 in the manifest.',
                     'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del all, manifest_validation_errors.csv')

    def test_not_valid_deletion_some_duplicates(self):
        """Test for when the accession matches the manifest due to only some duplicate files being deleted.
        Change is detected based on the number of files, not fixity.
        """
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_005_er')
        file = 'initialmanifest_20231031.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.05.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.05.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.05.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test005_005_er', '1 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(directory, '2023_test005_005_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Number of files does not match. 2 files in the accession folder and 4 in the manifest.',
                     'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with test for not valid/del some, manifest_validation_errors.csv')

    def test_not_valid_edit(self):
        """Test for when the accession does not match the manifest due to files being edited."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_002_er')
        file = 'initialmanifest_20230601.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.02.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.02.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.02.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test005_002_er', '4 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(directory, '2023_test005_002_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(root, '2023_test005_002_er', 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                    [join(root, '2023_test005_002_er', 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit, manifest_validation_errors.csv')

    def test_not_valid_edit_duplicates(self):
        """Test for when the accession does not match the manifest due to files being edited.
        The edited file was one of three copies. The other two copies were not edited."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_not_valid', '2023_test005_004_er')
        file = 'initialmanifest_20230521.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.04.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.04.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, preservation_log.txt')

        # Verifies the fixity validation CSV has the correct values.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Accession', 'Validation_Error'],
                    ['2023_test005_004_er', '1 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, fixity_validation.csv')

        # Verifies the manifest log has the correct values.
        result = csv_to_list(join(directory, '2023_test005_004_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [join(root, '2023_test005_004_er', 'CD_2', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for not valid/edit dup, manifest_validation_errors.csv')

    def test_valid(self):
        """Test for when the accession matches the manifest."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_001_er')
        file = 'initialmanifest_20231003.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.01.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.01.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T4.01.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')

        # Verifies the fixity validation CSV was not made.
        result = exists(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, 'Problem with test for valid, fixity_validation.csv')

        # Verifies the manifest log was not made.
        result = exists(join(directory, '2023_test004_001_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid, manifest_validation_errors.csv')

    def test_valid_duplicate(self):
        """Test for when the accession matches the manifest. It includes duplicate files."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_002_er')
        file = 'initialmanifest_20231124.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.02.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T4.02.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid + dups, preservation_log.txt')

        # Verifies the fixity validation CSV was not made.
        result = exists(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, 'Problem with test for valid + dups, fixity_validation.csv')

        # Verifies the manifest log was not made.
        result = exists(join(directory, '2023_test004_002_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + dups, manifest_validation_errors.csv')

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_003_er')
        file = 'initialmanifest_20240426.csv'
        directory = 'test_data'
        validate_manifest(root, file, directory)

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(join(root, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'JD'],
                    ['T4', '2023.T4.03.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.03.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T4.03.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid + FITS, preservation_log.txt')

        # Verifies the fixity validation CSV was not made.
        result = exists(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(result, False, 'Problem with test for valid + FITS, fixity_validation.csv')

        # Verifies the manifest log was not made.
        result = exists(join(directory, '2023_test004_003_er_manifest_validation_errors.csv'))
        self.assertEqual(result, False, 'Problem with test for valid + FITS, manifest_validation_errors.csv')


if __name__ == '__main__':
    unittest.main()
