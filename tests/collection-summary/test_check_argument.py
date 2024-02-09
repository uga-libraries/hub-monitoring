"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
"""
import os
import unittest
from collection_summary import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the directory argument is present and a valid path."""
        directory, error = check_argument([os.path.join(os.getcwd(),'..', 'collection_summary.py'),
                                           os.getcwd()])
        result = (directory, error)
        expected = (os.getcwd(), None)
        self.assertEqual(result, expected, "Problem with test for correct directory argument")

    def test_directory_missing(self):
        """Test for when the directory argument is not present."""
        directory, error = check_argument([os.path.join(os.getcwd(),'..', 'collection_summary.py')])
        result = (directory, error)
        expected = (None, "Missing required argument: directory")
        self.assertEqual(result, expected, "Problem with test for directory argument missing")

    def test_directory_invalid(self):
        """Test for when the directory argument is not a valid path."""
        directory, error = check_argument([os.path.join(os.getcwd(),'..', 'collection_summary.py'), "path/error"])
        result = (directory, error)
        expected = (None, "Provided directory path/error does not exist")
        self.assertEqual(result, expected, "Problem with test for correct directory argument")


if __name__ == '__main__':
    unittest.main()
