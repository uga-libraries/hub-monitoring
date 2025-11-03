"""
Tests for the function get_bag_size(), which gets the size of a bag from the Payload-Oxum in GB.

Note: other than the bag with size zero, these bags are not valid.
We updated the Payload-Oxum in bag-info.txt to test larger sizes without needing large bags in the repo.
"""
import os
import unittest
from validate_fixity import get_bag_size


class MyTestCase(unittest.TestCase):

    def test_zero(self):
        """Test for a bag small enough to round to zero"""
        # Makes the variable needed for function input and runs the function.
        bag_path = os.path.join('test_data', 'get_bag_size', 'zero_bag')
        bag_size = get_bag_size(bag_path)

        # Verifies the function returned the correct value for bag_size.
        self.assertEqual(0.0, bag_size, "Problem with test for zero")

    def test_fraction(self):
        """Test for a bag that is less than a GB"""
        # Makes the variable needed for function input and runs the function.
        bag_path = os.path.join('test_data', 'get_bag_size', 'fraction_bag')
        bag_size = get_bag_size(bag_path)

        # Verifies the function returned the correct value for bag_size.
        self.assertEqual(0.1, bag_size, "Problem with test for fraction")

    def test_gb(self):
        """Test for a bag that is more than a GB"""
        # Makes the variable needed for function input and runs the function.
        bag_path = os.path.join('test_data', 'get_bag_size', 'gb_bag')
        bag_size = get_bag_size(bag_path)

        # Verifies the function returned the correct value for bag_size.
        self.assertEqual(1.4, bag_size, "Problem with test for gb")


if __name__ == '__main__':
    unittest.main()
