"""
Tests for the function validate_bag(), which validates an accession's bag and returns the error message.
"""
import unittest
from validate_fixity import validate_bag
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_file_added(self):
        """Test for when the bag is not valid because a file was added"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_002_bags_invalid',
                       '2023_test002_001_er', '2023_test002_001_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes'
        self.assertEqual(validation, expected, 'Problem with test for file added')

    def test_file_deleted(self):
        """Test for when the bag is not valid because a file was deleted"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_002_bags_invalid',
                       '2023_test002_002_er', '2023_test002_002_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes'
        self.assertEqual(validation, expected, 'Problem with test for file deleted')

    def test_file_edited(self):
        """Test for when the bag is not valid because a file was edited"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_002_bags_invalid',
                       '2023_test002_003_er', '2023_test002_003_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 3 files and 79 bytes'
        self.assertEqual(validation, expected, 'Problem with test for file edited')

    def test_fixity_changed(self):
        """Test for when the bag is not valid because a file's fixity was changed in the manifest"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_002_bags_invalid',
                       '2023_test002_004_er', '2023_test002_004_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: ' \
                   'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'
        self.assertEqual(validation, expected, 'Problem with test for fixity changed')

    def test_missing_bag_info(self):
        """Test for when the bag is not valid because bag-info.txt is missing"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_002_bags_invalid',
                       '2023_test002_005_er', '2023_test002_005_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Bag validation failed: bag-info.txt exists in manifest but was not found on filesystem'
        self.assertEqual(validation, expected, 'Problem with test for missing bagit-info.txt')

    def test_valid(self):
        """Test for when the bag is valid"""
        bag_dir = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_001_bags_valid',
                       '2023_test001_001_er', '2023_test001_001_er_bag')
        validation = validate_bag(bag_dir)
        expected = 'Bag valid'
        self.assertEqual(validation, expected, 'Problem with test for valid bag')


if __name__ == '__main__':
    unittest.main()
