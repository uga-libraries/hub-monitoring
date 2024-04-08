"""
Tests for the function validate_manifest(), which validates an accession using a manifest
and returns if it is valid and the error message.
"""
import unittest
from validate_fixity import validate_manifest
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_valid_FITS(self):
        """Test for when the accession matches the manifest. It also has a FITS folder."""
        # Makes the variables for function input and runs the function.
        acc_path = join(getcwd(), '..', 'test_data', 'Validate_Fixity', 'test_004_manifest_valid', '2023_test004_003_er')
        manifest_path = join(acc_path, 'initialmanifest_20231124.csv')
        is_valid, error = validate_manifest(acc_path, manifest_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, None, 'Problem with test for valid FITS, is_valid')

        # Verifies error has the correct value.
        expected = None
        self.assertEqual(error, expected, 'Problem with test for valid FITS, error')


if __name__ == '__main__':
    unittest.main()
