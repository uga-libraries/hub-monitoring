"""
Tests for the function get_bag_size(), which gets the size of a bag from the Payload-Oxum in GB.

Note: we did not want to store a large enough bag to not be zero,
so use the template to test a bag on your local machine, if needed.
"""
import os
import unittest
from validate_fixity import get_bag_size


class MyTestCase(unittest.TestCase):

    def test_small_bag(self):
        """Test for a bag small enough to fit in the GitHub repo, which rounds to zero"""
        # Makes the variable needed for function input and runs the function.
        bag_path = os.path.join('test_data', 'get_bag_size', 'id_bag')
        bag_size = get_bag_size(bag_path)

        # Verifies the function returned the correct value for bag_size.
        self.assertEqual(0.0, bag_size, "Problem with test for small bag")

    # def test_template(self):
    #     """Test for a bag on a local computer, to be big enough to not be 0.0"""
    #     # Makes the variable needed for function input and runs the function.
    #     bag_path = 'INSERT PATH HERE'
    #     bag_size = get_bag_size(bag_path)
    #
    #     # Verifies the function returned the correct value for bag_size.
    #     expected = 'INSERT SIZE HERE'
    #     self.assertEqual(expected, bag_size, "Problem with test for local bag")


if __name__ == '__main__':
    unittest.main()
