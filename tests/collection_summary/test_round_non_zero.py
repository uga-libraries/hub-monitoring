"""
Tests for the function round_non_zero(), which rounds a number to the smallest number of decimal places
that don't result in 0.
"""
import unittest
from collection_summary import round_non_zero


class MyTestCase(unittest.TestCase):

    def test_0(self):
        """Test for a number with 0 decimal places"""
        size_gb = round_non_zero(42)
        self.assertEqual(42.00, size_gb, "Problem with test for 0 decimal places")

    def test_1(self):
        """Test for a number with 1 decimal place"""
        size_gb = round_non_zero(0.1)
        self.assertEqual(0.10, size_gb, "Problem with test for 1 decimal place")

    def test_2(self):
        """Test for a number with 2 decimal places"""
        size_gb = round_non_zero(0.99)
        self.assertEqual(0.99, size_gb, "Problem with test for 2 decimal places")

    def test_3_nonzero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is not zero"""
        size_gb = round_non_zero(3.032)
        self.assertEqual(3.03, size_gb, "Problem with test for 3 decimal places, 2 is not zero")

    def test_3_zero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is zero"""
        size_gb = round_non_zero(0.0007)
        self.assertEqual(0.001, size_gb, "Problem with test for 3 decimal places, 2 is zero")

    def test_6_zero(self):
        """Test for a number with 7 decimal places, where rounding to 2 or 3 is zero"""
        size_gb = round_non_zero(0.000123)
        self.assertEqual(0.0001, size_gb, "Problem with test for 7 decimal places, 2 and 3 is zero")

    def test_zero(self):
        """Test for when the number is zero"""
        size_gb = round_non_zero(0)
        self.assertEqual(0.00, size_gb, "Problem with test for zero")


if __name__ == '__main__':
    unittest.main()
