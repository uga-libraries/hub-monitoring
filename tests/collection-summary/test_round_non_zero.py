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
        self.assertEqual(round_number, 42.00, "problem with test for 0 decimal places")

    def test_1(self):
        """Test for a number with 1 decimal place"""
        round_number = round_non_zero(0.1)
        self.assertEqual(round_number, 0.10, "problem with test for 1 decimal place")

    def test_3_nonezero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is not zero"""
        round_number = round_non_zero(3.032)
        self.assertEqual(round_number, 3.03, "problem with test for 3 decimal places, 2 is not zero")

    def test_3_zero(self):
        """Test for a number with 3 decimal places, where rounding to 2 is zero"""
        round_number = round_non_zero(0.0007)
        self.assertEqual(round_number, 0.001, "problem with test for 3 decimal places, 2 is zero")

    def test_6_zero(self):
        """Test for a number with 7 decimal places, where rounding to 2 or 3 is zero"""
        round_number = round_non_zero(0.000123)
        self.assertEqual(round_number, 0.0001, "problem with test for 7 decimal places, 2 and 3 is zero")


if __name__ == '__main__':
    unittest.main()