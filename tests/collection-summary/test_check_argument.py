"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
In production, the input is from sys.argv
"""
import unittest
from collection_summary import check_argument
from os import getcwd


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the directory argument is present and a valid path."""
        result = check_argument(['collection_summary.py', getcwd()])
        expected = (getcwd(), None)
        self.assertEqual(result, expected, "Problem with test for correct directory argument")

    def test_directory_missing(self):
        """Test for when the directory argument is not present."""
        result = check_argument(['collection_summary.py'])
        expected = (None, "Missing required argument: directory")
        self.assertEqual(result, expected, "Problem with test for directory argument missing")

    def test_directory_invalid(self):
        """Test for when the directory argument is not a valid path."""
        result = check_argument(['collection_summary.py', 'path/error'])
        expected = (None, "Provided directory path/error does not exist")
        self.assertEqual(result, expected, "Problem with test for correct directory argument")

    def test_extra_argument(self):
        """Test for when there are too many arguments provided."""
        result = check_argument(['collection_summary.py', getcwd(), 'extra'])
        expected = (None, "Missing required argument: directory")
        self.assertEqual(result, expected, "Problem with test for directory argument missing")


if __name__ == '__main__':
    unittest.main()
