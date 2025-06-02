"""
Tests for the function check_argument(), which verifies the required argument is present and a valid path.
In production, the input is from sys.argv
"""
import os
import unittest
from validate_fixity import check_argument


class MyTestCase(unittest.TestCase):

    def test_correct_born_digital(self):
        """Test for when the directory argument is present and a valid path to "born-digital"."""
        # Makes variables for function input and runs the function.
        input_dir = os.path.join('test_data', 'test_script_restart', 'born-digital')
        sys_argv = ['validate_fixity.py', input_dir]
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, input_dir, 'Problem with test for born-digital, input_directory')

        # Checks error has the correct value.
        self.assertEqual(error, None, 'Problem with test for born-digital, error')

    def test_correct_Born_digital(self):
        """Test for when the directory argument is present and a valid path to "Born-digital"."""
        # Makes variables for function input and runs the function.
        input_dir = os.path.join('test_data', 'test_script_valid', 'Born-digital')
        sys_argv = ['validate_fixity.py', input_dir]
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, input_dir, 'Problem with test for Born-digital, input_directory')

        # Checks error has the correct value.
        self.assertEqual(error, None, 'Problem with test for Born-digital, error')

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

    def test_directory_not_born_digital(self):
        """Test for when the directory argument is a valid path but not the expected name."""
        # Makes variable for function input and runs the function.
        sys_argv = ['validate_fixity.py', 'test_data']
        input_directory, error = check_argument(sys_argv)

        # Checks input_directory has the correct value.
        self.assertEqual(input_directory, None, 'Problem with test for directory not b-d, input_directory')

        # Checks error has the correct value.
        expected = "Provided input_directory 'test_data' is not to folder 'Born-digital' or 'born-digital'"
        self.assertEqual(error, expected, 'Problem with test for directory not b-d, error')

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
