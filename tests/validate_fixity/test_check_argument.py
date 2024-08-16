"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
In production, the input is from sys.argv
"""
import unittest
from validate_fixity import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the directory argument is present and a valid path."""
        # Makes variable for function input and runs the function.
        sys_argv = ['validate_fixity.py', 'test_data']
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, 'test_data', 'Problem with test for correct, input_directory')

        # Checks error has the correct value.
        self.assertEqual(error, None, 'Problem with test for correct, error')

    def test_directory_missing(self):
        """Test for when the directory argument is not present."""
        # Makes variable for function input and runs the function.
        sys_argv = ['validate_fixity.py']
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, None, 'Problem with test for directory missing, input_directory')

        # Checks error has the correct value.
        expected = 'Missing required argument: input_directory'
        self.assertEqual(error, expected, 'Problem with test for directory missing, error')

    def test_directory_invalid(self):
        """Test for when the directory argument is not a valid path."""
        # Makes variable for function input and runs the function.
        sys_argv = ['validate_fixity.py', 'path/error']
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, None, 'Problem with test for directory invalid, input_directory')

        # Checks error has the correct value.
        expected = "Provided input_directory 'path/error' does not exist"
        self.assertEqual(error, expected, 'Problem with test for invalid directory invalid, error')

    def test_extra_argument(self):
        """Test for when there are too many arguments provided."""
        # Makes variable for function input and runs the function.
        sys_argv = ['validate_fixity.py', 'test_data', 'extra']
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, None, 'Problem with test for extra argument, input_directory')

        # Checks error has the correct value.
        expected = 'Too many arguments. Should just have one argument, input_directory'
        self.assertEqual(error, expected, 'Problem with test for extra argument, error')


if __name__ == '__main__':
    unittest.main()
