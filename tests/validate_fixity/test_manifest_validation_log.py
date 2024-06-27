"""
Tests for the function manifest_validation_log(), which saves validation errors to a text file.

To simplify the test data needed, the errors_list does not match the directory.
"""
import unittest
from validate_fixity import manifest_validation_log
from test_script_validate_fixity import csv_to_list
from os import remove
from os.path import basename, exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        if exists(join('test_data', 'test_005_manifest_not_valid', '2023_test005_001_er_manifest_validation_errors.csv')):
            remove(join('test_data', 'test_005_manifest_not_valid', '2023_test005_001_er_manifest_validation_errors.csv'))

    def test_both(self):
        """Test for when the errors are from file count and fixity differences"""
        # Makes variables for function input and runs the function.
        directory = join('test_data', 'test_005_manifest_not_valid')
        root = join(directory, '2023_test005_001_er')
        errors_list = [['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                       [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current'],
                       ['Number of files does not match. 2 files in the accession folder and 3 in the manifest.']]
        manifest_validation_log(directory, basename(root), errors_list)

        # Verifies the report has the correct values.
        result = csv_to_list(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current'],
                    ['Number of files does not match. 2 files in the accession folder and 3 in the manifest.', 'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with test for fixity')

    def test_files(self):
        """Test for when the errors are from file count differences"""
        # Makes variables for function input and runs the function.
        directory = join('test_data', 'test_005_manifest_not_valid')
        root = join(directory, '2023_test005_001_er')
        errors_list = [['Number of files does not match. 3 files in the accession folder and 4 in the manifest.']]
        manifest_validation_log(directory, basename(root), errors_list)

        # Verifies the report has the correct values.
        result = csv_to_list(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Number of files does not match. 3 files in the accession folder and 4 in the manifest.', 'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with test for files')

    def test_fixity(self):
        """Test for when the errors are from fixity differences"""
        # Makes variables for function input and runs the function.
        directory = join('test_data', 'test_005_manifest_not_valid')
        root = join(directory, '2023_test005_001_er')
        errors_list = [['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                       ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                       [join(root, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                       [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        manifest_validation_log(directory, basename(root), errors_list)

        # Verifies the report has the correct values.
        result = csv_to_list(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(root, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                    [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        self.assertEqual(result, expected, 'Problem with test for fixity')


if __name__ == '__main__':
    unittest.main()
