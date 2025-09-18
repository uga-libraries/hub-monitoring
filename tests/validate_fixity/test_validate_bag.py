"""
Tests for the function validate_bag(), which validates an accession's bag and returns information for the logs.
"""
import os
import unittest
from validate_fixity import validate_bag


class MyTestCase(unittest.TestCase):

    def test_file_added(self):
        """Test for when the bag is not valid because a file was added"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test002_001_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test002_001_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes'
        self.assertEqual(result, expected, 'Problem with test for file added')

    def test_file_deleted(self):
        """Test for when the bag is not valid because a file was deleted"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test002_002_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test002_002_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes'
        self.assertEqual(result, expected, 'Problem with test for file deleted')

    def test_file_edited(self):
        """Test for when the bag is not valid because a file was edited"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test002_003_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test002_003_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 3 files and 79 bytes'
        self.assertEqual(result, expected, 'Problem with test for file edited')

    def test_fixity_changed(self):
        """Test for when the bag is not valid because a file's fixity was changed in the manifest"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test002_004_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test002_004_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = ('Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                    'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"')
        self.assertEqual(result, expected, 'Problem with test for fixity changed')

    def test_missing_bag_info(self):
        """Test for when the bag is not valid because bag-info.txt is missing"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test002_005_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test002_005_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Bag validation failed: bag-info.txt exists in manifest but was not found on filesystem'
        self.assertEqual(result, expected, 'Problem with test for missing bag-info.txt')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_bag', '2023_test001_001_er')
        input_directory = 'test_data'
        result = validate_bag(accession_path, input_directory, '2023_test001_001_er_bag')

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(result, expected, 'Problem with test for valid')


if __name__ == '__main__':
    unittest.main()
