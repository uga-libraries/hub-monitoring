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
        sys_argv = ['risk_updates.py', join('..', 'test_data'), join('..', 'test_data', 'NARA_PreservationActionPlan.csv')]
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = '..\\test_data'
        self.assertEqual(directory, expected, 'Problem with both correct, directory')

        # Tests that the value of nara_csv is correct.
        expected = '..\\test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with both correct, nara_csv')
        
        # Tests that the value of errors_list is correct.
        self.assertEqual(errors_list, [], 'Problem with both correct, errors_list')

    def test_both_missing(self):
        """
        Test for when neither required argument is present.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py']
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        self.assertEqual(directory, None, 'Problem with both missing, directory')

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, 'Problem with both missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument directory is missing',
                    'Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with both missing, errors_list')

    def test_both_path_error(self):
        """
        Test for when both required arguments are present but are not valid paths.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', 'error/directory', 'error/NARA_PreservationActionPlan.csv']
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = 'error/directory'
        self.assertEqual(directory, expected, 'Problem with both path error, directory')

        # Tests that the value of nara_csv is correct.
        expected = 'error/NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with both path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["Directory 'error/directory' does not exist",
                    "NARA CSV 'error/NARA_PreservationActionPlan.csv' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with both path error, errors_list')

    def test_directory_missing(self):
        """
        Test for when the first required argument directory is not present.
        The second required argument, nara_csv, is present and valid,
        so the function treats it as directory.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('..', 'test_data', 'NARA_PreservationActionPlan.csv')]
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = '..\\test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(directory, expected, 'Problem with directory missing, directory')

        # Tests that the value of nara_csv is correct.
        expected = None
        self.assertEqual(nara_csv, expected, 'Problem with directory missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with directory missing, errors_list')

    def test_directory_path_error(self):
        """
        Test for when the first required argument directory is present but not a valid path.
        The second required argument, nara_csv, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', 'path/error/dir', join('..', 'test_data', 'NARA_PreservationActionPlan.csv')]
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = 'path/error/dir'
        self.assertEqual(directory, expected, 'Problem with directory path error, directory')

        # Tests that the value of nara_csv is correct.
        expected = '..\\test_data\\NARA_PreservationActionPlan.csv'
        self.assertEqual(nara_csv, expected, 'Problem with directory path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["Directory 'path/error/dir' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with directory path error, errors_list')

    def test_nara_missing(self):
        """
        Test for when the second required argument nara_csv is not present.
        The first required argument, directory, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('..', 'test_data')]
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = '..\\test_data'
        self.assertEqual(directory, expected, 'Problem with NARA missing, directory')

        # Tests that the value of nara_csv is correct.
        self.assertEqual(nara_csv, None, 'Problem with NARA missing, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ['Required argument nara_csv is missing']
        self.assertEqual(errors_list, expected, 'Problem with NARA missing, errors_list')

    def test_nara_path_error(self):
        """
        Test for when the second required argument nara_csv is present but not a valid path.
        The first required argument, directory, is present and valid.
        """
        # Makes the variable used for function input and runs the function being tested.
        sys_argv = ['risk_updates.py', join('..', 'test_data'), 'nara_error.csv']
        directory, nara_csv, errors_list = check_arguments(sys_argv)

        # Tests that the value of directory is correct.
        expected = '..\\test_data'
        self.assertEqual(directory, expected, 'Problem with NARA path error, directory')

        # Tests that the value of nara_csv is correct.
        expected = 'nara_error.csv'
        self.assertEqual(nara_csv, expected, 'Problem with NARA path error, nara_csv')

        # Tests that the value of errors_list is correct.
        expected = ["NARA CSV 'nara_error.csv' does not exist"]
        self.assertEqual(errors_list, expected, 'Problem with NARA path error, errors_list')


if __name__ == '__main__':
    unittest.main()
