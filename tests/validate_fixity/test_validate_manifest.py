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
        acc_path = join('test_data', 'test_005_manifest_invalid', '2023_test005_001_er')
        manifest_path = join(acc_path, 'initialmanifest_20230501.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid deletion, is_valid')

        # Verifies error has the correct value.
        expected_error = [['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest']]
        self.assertEqual(error, expected_error, 'Problem with test for invalid deletion, error')

    def test_invalid_edit(self):
        """Test for when the accession does not match the manifest due to files being edited."""
        # Makes the variables for function input and runs the function.
        acc_path = join('test_data', 'test_005_manifest_invalid', '2023_test005_002_er')
        manifest_path = join(acc_path, 'initialmanifest_20230601.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for invalid edit, is_valid')

        # Verifies error has the correct value.
        accession = join('test_data', 'test_005_manifest_invalid', '2023_test005_002_er', '2023_test005_002_er')
        expected_error = [['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                          ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                          [join(accession, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                          [join(accession, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        self.assertEqual(error, expected_error, 'Problem with test for invalid edit, error')

    def test_valid(self):
        """Test for when the accession matches the manifest."""
        # Makes the variables for function input and runs the function.
        acc_path = join('test_data', 'test_004_manifest_valid', '2023_test004_001_er')
        manifest_path = join(acc_path, 'initialmanifest_20231003.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid, is_valid')

        # Verifies error has the correct value.
        expected_error = []
        self.assertEqual(error, expected_error, 'Problem with test for valid, error')

    def test_valid_duplicate(self):
        """Test for when the accession matches the manifest."""
        # Makes the variables for function input and runs the function.
        acc_path = join('test_data', 'test_004_manifest_valid', '2023_test004_002_er')
        manifest_path = join(acc_path, 'initialmanifest_20231124.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid duplicate, is_valid')

        # Verifies error has the correct value.
        expected_error = []
        self.assertEqual(error, expected_error, 'Problem with test for valid duplicate, error')

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        acc_path = join('test_data', 'test_004_manifest_valid', '2023_test004_003_er')
        manifest_path = join(acc_path, 'initialmanifest_20240426.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid FITS, is_valid')

        # Verifies error has the correct value.
        expected_error = []
        self.assertEqual(error, expected_error, 'Problem with test for valid FITS, error')


if __name__ == '__main__':
    unittest.main()
