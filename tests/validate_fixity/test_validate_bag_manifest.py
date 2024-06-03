"""
Start for tests for the function validate_bag_manifest(), which validates an accession using the bag manifest
if bagit cannot do the validation.

At this point, it is just running a valid and not valid bag through the function for initial development,
with print statements in the function showing the value.
Once we confirm this is working on real data, these will be made into real tests.
"""
import unittest
from validate_fixity import validate_bag_manifest
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_not_valid(self):
        """Test for when the bag is not valid"""
        bag_dir = join('test_data', 'test_002_bags_invalid', '2023_test002_001_er', '2023_test002_001_er_bag')
        validate_bag_manifest(bag_dir)
        self.assertEqual(False, False)  # add assertion here

    def test_valid(self):
        """Test for when the bag is valid"""
        bag_dir = join('test_data', 'test_001_bags_valid', '2023_test001_002_er', '2023_test001_002_er_bag')
        validate_bag_manifest(bag_dir)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
