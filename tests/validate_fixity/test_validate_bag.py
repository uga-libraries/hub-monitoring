"""
Tests for the function validate_bag(), which validates an accession's bag
and returns if it is valid and the error message.
"""
import unittest
from validate_fixity import validate_bag
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_file_added(self):
        """Test for when the bag is not valid because a file was added"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', '2023_test002_001_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file added, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes'
        self.assertEqual(error, expected, 'Problem with test for file added, error')

    def test_file_deleted(self):
        """Test for when the bag is not valid because a file was deleted"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_002_bags_invalid', '2023_test002_002_er', '2023_test002_002_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file deleted, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes'
        self.assertEqual(error, expected, 'Problem with test for file deleted, error')

    def test_file_edited(self):
        """Test for when the bag is not valid because a file was edited"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_002_bags_invalid', '2023_test002_003_er', '2023_test002_003_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file edited, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 3 files and 79 bytes'
        self.assertEqual(error, expected, 'Problem with test for file edited, error')

    def test_fixity_changed(self):
        """Test for when the bag is not valid because a file's fixity was changed in the manifest"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_002_bags_invalid', '2023_test002_004_er', '2023_test002_004_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for fixity changed, is_valid')

        # Verifies error has the correct value.
        expected = 'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: ' \
                   'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'
        self.assertEqual(error, expected, 'Problem with test for fixity changed, error')

    def test_missing_bag_info(self):
        """Test for when the bag is not valid because bag-info.txt is missing"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_002_bags_invalid', '2023_test002_005_er', '2023_test002_005_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for missing bag-info.txt, is_valid')

        # Verifies error has the correct value.
        expected = 'Bag validation failed: bag-info.txt exists in manifest but was not found on filesystem'
        self.assertEqual(error, expected, 'Problem with test for missing bag-info.txt, error')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes variable for function input and runs the function.
        bag_path = join('test_data', 'test_001_bags_valid', '2023_test001_001_er', '2023_test001_001_er_bag')
        is_valid, error = validate_bag(bag_path)

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid, is_valid')

        # Verifies error has the correct value.
        expected = None
        self.assertEqual(error, expected, 'Problem with test for valid bag, error')


if __name__ == '__main__':
    unittest.main()
