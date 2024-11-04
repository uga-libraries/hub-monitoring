"""
Tests for the function check_arguments(),
which verifies the two required arguments are present and are valid paths,
and returns the paths and a list of errors (if any).

For input, tests use a list with argument values. In production, this would be the contents of sys.argv.
"""
import unittest
from os.path import join
from risk_update import check_arguments


class MyTestCase(unittest.TestCase):

    def test_both_correct(self):
        """
        Test for when both required arguments are present and valid paths.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('test_data', 'script'),
                    join('test_data', 'NARA_PreservationActionPlan.csv')]
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'test_data\\script'
        self.assertEqual(input_directory, expected, 'Problem with both correct, input_directory')

        # Tests that the value of nara_csv is correct.
        expected = 'test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with both correct, nara_csv')
        
        # Tests that the value of errors_list is correct.
        self.assertEqual(errors_list, [], 'Problem with both correct, errors_list')

    def test_both_missing(self):
        """
        Test for when neither required argument is present.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py']
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        self.assertEqual(input_directory, None, 'Problem with both missing, input_directory')

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, 'Problem with both missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument input_directory is missing', 'Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with both missing, errors_list')

    def test_both_path_error(self):
        """
        Test for when both required arguments are present but are not valid paths.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', 'error/input_directory', 'error/NARA_PreservationActionPlan.csv']
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'error/input_directory'
        self.assertEqual(input_directory, expected, 'Problem with both path error, input_directory')

        # Tests that the value of nara_csv is correct.
        expected = 'error/NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with both path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["Input directory 'error/input_directory' does not exist",
                    "NARA CSV 'error/NARA_PreservationActionPlan.csv' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with both path error, errors_list')

    def test_input_directory_missing(self):
        """
        Test for when the first required argument input_directory is not present.
        The second required argument, nara_csv, is present and valid,
        so the function treats it as input_directory.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('test_data', 'NARA_PreservationActionPlan.csv')]
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(input_directory, expected, 'Problem with input_directory missing, input_directory')

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, 'Problem with input_directory missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with input_directory missing, errors_list')

    def test_input_directory_path_error(self):
        """
        Test for when the first required argument input_directory is present but not a valid path.
        The second required argument, nara_csv, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', 'path/error/dir', join('test_data', 'NARA_PreservationActionPlan.csv')]
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'path/error/dir'
        self.assertEqual(input_directory, expected, 'Problem with input_directory path error, input_directory')

        # Tests that the value of nara_csv is correct.
        expected = 'test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with input_directory path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["Input directory 'path/error/dir' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with input_directory path error, errors_list')

    def test_nara_missing(self):
        """
        Test for when the second required argument nara_csv is not present.
        The first required argument, input_directory, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('test_data', 'script')]
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'test_data\\script'
        self.assertEqual(input_directory, expected, 'Problem with NARA missing, input_directory')

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, 'Problem with NARA missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with NARA missing, errors_list')

    def test_nara_path_error(self):
        """
        Test for when the second required argument nara_csv is present but not a valid path.
        The first required argument, input_directory, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('test_data\\script'), 'nara_error.csv']
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'test_data\\script'
        self.assertEqual(input_directory, expected, 'Problem with NARA path error, input_directory')

        # Tests that the value of nara_csv is correct.
        expected = 'nara_error.csv'
        self.assertEqual(nara_csv, expected, 'Problem with NARA path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["NARA CSV 'nara_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with NARA path error, errors_list')

    def test_too_many_arguments(self):
        """
        Test for when there is an extra argument.
        The two required arguments are present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('test_data', 'script'),
                    join('test_data', 'NARA_PreservationActionPlan.csv'), 'error_extra_argument']
        input_directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of input_directory is correct.
        expected = 'test_data\\script'
        self.assertEqual(input_directory, expected, 'Problem with too many arguments, input_directory')

        # Tests that the value of nara_csv is correct.
        expected = 'test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with too many arguments, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Too many arguments. Should just have two, input_directory and nara_csv']
        self.assertEqual(errors_list, expected, 'Problem with too many arguments, errors_list')


if __name__ == '__main__':
    unittest.main()
