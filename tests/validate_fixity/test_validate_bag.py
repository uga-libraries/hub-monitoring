"""
Tests for the function validate_bag(), which validates an accession's bag
and returns if it is valid and the error message.
"""
import unittest
from validate_fixity import validate_bag
from os.path import join


class MyTestCase(unittest.TestCase):

    # def test_bag_error(self):
    #     """Template for test for when the bag cannot be validated because bagit gives a BagError
    #     This is caused by path length and cannot be reliably replicated in the test data.
    #     Instead, supply the path in root and folder to a bag known to have this error.
    #     """
    #     # Makes variables for function input and runs the function.
    #     root = 'INSERT PATH TO ACCESSION FOLDER'
    #     folder = 'INSERT NAME OF BAG FOLDER'
    #     is_valid, error = validate_bag(join(root, folder))
    #
    #     # Verifies is_valid has the correct value.
    #     self.assertEqual(is_valid, False, 'Problem with test for bag error, is_valid')
    #
    #     # Verifies error has the correct value.
    #     expected = 'Cannot make bag for validation: INSERT ERROR FROM VALIDATING BAG WITH BAGIT'
    #     self.assertEqual(error, expected, 'Problem with test for bag error, error')

    def test_file_added(self):
        """Test for when the bag is not valid because a file was added"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er')
        folder = '2023_test002_001_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file added, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 4 files and 90 bytes'
        self.assertEqual(error, expected, 'Problem with test for file added, error')

    def test_file_deleted(self):
        """Test for when the bag is not valid because a file was deleted"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_002_er')
        folder = '2023_test002_002_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file deleted, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 2 files and 38 bytes'
        self.assertEqual(error, expected, 'Problem with test for file deleted, error')

    def test_file_edited(self):
        """Test for when the bag is not valid because a file was edited"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_003_er')
        folder = '2023_test002_003_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for file edited, is_valid')

        # Verifies error has the correct value.
        expected = 'Payload-Oxum validation failed. Expected 3 files and 47 bytes but found 3 files and 79 bytes'
        self.assertEqual(error, expected, 'Problem with test for file edited, error')

    def test_fixity_changed(self):
        """Test for when the bag is not valid because a file's fixity was changed in the manifest"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_004_er')
        folder = '2023_test002_004_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for fixity changed, is_valid')

        # Verifies error has the correct value.
        expected = 'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: ' \
                   'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'
        self.assertEqual(error, expected, 'Problem with test for fixity changed, error')

    def test_missing_bag_info(self):
        """Test for when the bag is not valid because bag-info.txt is missing"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_002_bags_invalid', '2023_test002_005_er')
        folder = '2023_test002_005_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, False, 'Problem with test for missing bag-info.txt, is_valid')

        # Verifies error has the correct value.
        expected = 'Bag validation failed: bag-info.txt exists in manifest but was not found on filesystem'
        self.assertEqual(error, expected, 'Problem with test for missing bag-info.txt, error')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes variables for function input and runs the function.
        root = join('test_data', 'test_001_bags_valid', '2023_test001_001_er')
        folder = '2023_test001_001_er_bag'
        is_valid, error = validate_bag(join(root, folder))

        # Verifies is_valid has the correct value.
        self.assertEqual(is_valid, True, 'Problem with test for valid, is_valid')

        # Verifies error has the correct value.
        self.assertEqual(error, None, 'Problem with test for valid bag, error')


if __name__ == '__main__':
    unittest.main()
