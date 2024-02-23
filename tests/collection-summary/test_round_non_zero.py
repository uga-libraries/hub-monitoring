"""
Tests for the function round_non_zero(), which rounds a number to the smallest number of decimal places
that don't result in 0.
"""
import unittest
from collection_summary import round_non_zero


class MyTestCase(unittest.TestCase):

    def test_0(self):
        """Test for a number with 0 decimal places"""
        round_number = round_non_zero(42)
        self.assertEqual(round_number, 42.00, "Problem with test for 0 decimal places")

    def test_1(self):
        """Test for a number with 1 decimal place"""
        round_number = round_non_zero(0.1)
        self.assertEqual(round_number, 0.10, "Problem with test for 1 decimal place")

    def test_2(self):
        """Test for a number with 2 decimal places"""
        round_number = round_non_zero(0.99)
        self.assertEqual(round_number, 0.99, "Problem with test for 2 decimal places")

    def test_3_nonzero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is not zero"""
        round_number = round_non_zero(3.032)
        self.assertEqual(round_number, 3.03, "Problem with test for 3 decimal places, 2 is not zero")

    def test_3_zero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is zero"""
        round_number = round_non_zero(0.0007)
        self.assertEqual(round_number, 0.001, "Problem with test for 3 decimal places, 2 is zero")

    def test_6_zero(self):
        """Test for a number with 7 decimal places, where rounding to 2 or 3 is zero"""
        round_number = round_non_zero(0.000123)
        self.assertEqual(round_number, 0.0001, "Problem with test for 7 decimal places, 2 and 3 is zero")

    def test_zero(self):
        """Test for when the number is zero"""
        round_number = round_non_zero(0)
        self.assertEqual(round_number, 0.00, "Problem with test for zero")


if __name__ == '__main__':
    unittest.main()