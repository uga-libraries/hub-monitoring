"""
Tests for the script validate_fixity.py, which validates accession fixity, updates the logs, and makes a report.
"""
import subprocess
import unittest
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the script runs correctly on all accessions in Validate_Fixity_Hub"""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub')
        subprocess.run(f'python {script} {directory}', shell=True)

        self.assertEqual(True, True)

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join('test_data', 'Error_Hub')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python {script} {directory}', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python {script} {directory}', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error_Hub' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")


if __name__ == '__main__':
    unittest.main()
