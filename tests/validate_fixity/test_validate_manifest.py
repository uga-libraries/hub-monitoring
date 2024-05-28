"""
Tests for the function validate_manifest(), which validates an accession using a manifest
and returns if it is valid and the error message.
"""
import unittest
from validate_fixity import validate_manifest
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_invalid_deletion(self):
        """Test for when the accession does not match the manifest due to file deletions."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_invalid', '2023_test005_001_er')
        file = 'initialmanifest_20230501.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid deletion, is_valid')

        # Verifies errors_list has the correct value.
        expected = [['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest'],
                    'Number of files does not match. 1 files in the accession folder and 2 in the manifest.']
        self.assertEqual(errors_list, expected, 'Problem with test for invalid deletion, error')

    def test_invalid_deletion_duplicates(self):
        """Test for when the accession does not match the manifest due to file deletions.
        All copies of a duplicate file have been deleted."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_invalid', '2023_test005_003_er')
        file = 'initialmanifest_20230511.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid deletion duplicates, is_valid')

        # Verifies errors_list has the correct value.
        expected = [['Z:\\2023_test005_003_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    ['Z:\\2023_test005_003_er\\CD_2\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    'Number of files does not match. 1 files in the accession folder and 3 in the manifest.']
        self.assertEqual(errors_list, expected, 'Problem with test for invalid deletion duplicates, error')

    def test_invalid_edit(self):
        """Test for when the accession does not match the manifest due to files being edited."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_invalid', '2023_test005_002_er')
        file = 'initialmanifest_20230601.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid edit, is_valid')

        # Verifies errors_list has the correct value.
        acc_path = join('test_data', 'test_005_manifest_invalid', '2023_test005_002_er', '2023_test005_002_er')
        expected = [['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(acc_path, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                    [join(acc_path, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        self.assertEqual(errors_list, expected, 'Problem with test for invalid edit, error')

    def test_invalid_edit_duplicates(self):
        """Test for when the accession does not match the manifest due to files being edited.
        The edited file was one of three copies. The other two copies were not edited."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_005_manifest_invalid', '2023_test005_004_er')
        file = 'initialmanifest_20230521.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid edit duplicates, is_valid')

        # Verifies errors_list has the correct value.
        # Since the duplicates in the current folder matched the manifest, the edited file only has an error in Current.
        acc_path = join('test_data', 'test_005_manifest_invalid', '2023_test005_004_er', '2023_test005_004_er')
        expected = [[join(acc_path, 'CD_2', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current']]
        self.assertEqual(errors_list, expected, 'Problem with test for invalid edit, error')

    def test_valid(self):
        """Test for when the accession matches the manifest."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_001_er')
        file = 'initialmanifest_20231003.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid, is_valid')

        # Verifies errors_list has the correct value.
        self.assertEqual(errors_list, [], 'Problem with test for valid, error')

    def test_invalid_deletion_some_duplicates(self):
        """Test for when the accession matches the manifest due to only some duplicate files being deleted.
        Change is detected based on the number of files, not fixity..
        """
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_004_er')
        file = 'initialmanifest_20231031.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid deletion some duplicates, is_valid')

        # Verifies errors_list has the correct value.
        expected = ['Number of files does not match. 2 files in the accession folder and 4 in the manifest.']
        self.assertEqual(errors_list, expected, 'Problem with test for invalid deletion some duplicates, error')

    def test_valid_duplicate(self):
        """Test for when the accession matches the manifest. It includes duplicate files."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_002_er')
        file = 'initialmanifest_20231124.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid duplicate, is_valid')

        # Verifies errors_list has the correct value.
        self.assertEqual(errors_list, [], 'Problem with test for valid duplicate, error')

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        root = join('test_data', 'test_004_manifest_valid', '2023_test004_003_er')
        file = 'initialmanifest_20240426.csv'
        is_valid, errors_list = validate_manifest(root, file)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid FITS, is_valid')

        # Verifies errors_list has the correct value.
        self.assertEqual(errors_list, [], 'Problem with test for valid FITS, error')


if __name__ == '__main__':
    unittest.main()
