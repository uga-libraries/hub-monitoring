import unittest
from validate_fixity import validate_bag_manifest
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_valid(self):
        """Test for when the bag is valid"""
        bag_dir = join('test_data', 'test_001_bags_valid', '2023_test001_002_er', '2023_test001_002_er_bag')
        validate_bag_manifest(bag_dir)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
