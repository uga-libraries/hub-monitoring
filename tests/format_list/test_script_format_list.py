"""
Tests for the script format_list.py
"""
import unittest
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv
from subprocess import CalledProcessError, PIPE, run


def csv_to_list(csv_path):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = read_csv(csv_path)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        if exists(join('test_data', 'combined_format_data.csv')):
            remove(join('test_data', 'combined_format_data.csv'))

    def test_correct(self):
        script = join(getcwd(), '..', '..', 'format_list.py')
        directory = 'test_data'
        run(f'python "{script}" "{directory}"', shell=True, stdout=PIPE)

        result = csv_to_list(join('test_data', 'combined_format_data.csv'))
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count', 'Size_GB'],
                    ['JPEG File Interchange Format', '1.01', 'Low Risk', 2, 82.858],
                    ['JPEG File Interchange Format', '1.02', 'Low Risk', 3, 0.183],
                    ['PDF/A', '1b', 'Low Risk', 1, 45.837],
                    ['Plain text', 'nan', 'Moderate Risk', 1, 5.113],
                    ['Portable Document Format', '1.4', 'Moderate Risk', 2, 0.504],
                    ['Portable Network Graphics', '1', 'High Risk', 1, 205.688],
                    ['Portable Network Graphics', '1', 'Moderate Risk', 1, 257.638],
                    ['Unknown Binary', 'nan', 'No Match', 1, 0.0]]
        self.assertEqual(result, expected, 'Problem with test for correct')

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'format_list.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(CalledProcessError):
            run(f'python "{script}" "{directory}"', shell=True, check=True, stdout=PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = run(f'python "{script}" "{directory}"', shell=True, stdout=PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, 'Problem with test for printed error')


if __name__ == '__main__':
    unittest.main()
