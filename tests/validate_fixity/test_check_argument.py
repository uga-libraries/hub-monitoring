"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
In production, the input is from sys.argv
"""
import unittest
from validate_fixity import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the directory argument is present and a valid path."""
        sys_argv = ['validate_fixity.py', 'test_data']
        result = check_argument(sys_argv)
        expected = ('test_data', None)
        self.assertEqual(result, expected, 'Problem with test for correct directory argument')

    def test_directory_missing(self):
        """Test for when the directory argument is not present."""
        sys_argv = ['validate_fixity.py']
        result = check_argument(sys_argv)
        expected = (None, 'Missing required argument: input_directory')
        self.assertEqual(result, expected, 'Problem with test for directory argument missing')

    def test_directory_invalid(self):
        """Test for when the directory argument is not a valid path."""
        sys_argv = ['validate_fixity.py', 'path/error']
        result = check_argument(sys_argv)
        expected = (None, "Provided input_directory 'path/error' does not exist")
        self.assertEqual(result, expected, 'Problem with test for correct directory argument')

    def test_extra_argument(self):
        """Test for when there are too many arguments provided."""
        sys_argv = ['validate_fixity.py', 'test_data', 'extra']
        result = check_argument(sys_argv)
        expected = (None, 'Too many arguments. Should just have one argument, input_directory')
        self.assertEqual(result, expected, 'Problem with test for extra argument')


if __name__ == '__main__':
    unittest.main()
