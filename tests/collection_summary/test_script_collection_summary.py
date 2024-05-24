"""
Tests for the script collection_summary.py, which makes a CSV summarizing the collections in a directory.
"""
import unittest
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv
from subprocess import CalledProcessError, PIPE, run


def csv_to_list(csv_path):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Date is made a string so the compared value is shorter.
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = read_csv(csv_path, dtype={'Date': str})
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test outputs if they were created"""
        # List of paths for possible test outputs.
        today = datetime.today().strftime('%Y-%m-%d')
        outputs = [join('test_data', 'Hargrett_Hub', f'hub-collection-summary_{today}.csv'),
                   join('test_data', 'Russell_Hub', f'hub-collection-summary_{today}.csv')]

        # Deletes any test output that is present.
        for output in outputs:
            if exists(output):
                remove(output)

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables needed for the script input.
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(CalledProcessError):
            run(f'python "{script}" "{directory}"', shell=True, check=True, stdout=PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = run(f'python "{script}" "{directory}"', shell=True, stdout=PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")

    def test_hargrett(self):
        """Test running the script with Hargrett test data"""
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        directory = join('test_data', 'Hargrett_Hub')
        run(f'python "{script}" "{directory}"', shell=True)

        report_path = join(directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(report_path)
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['ms0001 Person papers', '2024', 'backlogged', 0.00001, 3, 0, 0, 1, 2, 'nan'],
                    ['ua01-001 Dept records', '2024', 'backlogged', 0.00004, 4, 1, 0, 1, 2, 'nan']]
        self.assertEqual(result, expected, "Problem with test for Hargrett data")

    def test_russell(self):
        """Test running the script with Russell test data"""
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        directory = join('test_data', 'Russell_Hub')
        run(f'python "{script}" "{directory}"', shell=True, stdout=PIPE)

        # Tests the contents of the report.
        report_path = join(directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(report_path)
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['rbrl001', '2024', 'backlogged', 0.0002, 11, 0, 0, 0, 11, 'nan'],
                    ['rbrl002', '2024', 'backlogged', 0.0003, 41, 10, 9, 11, 12,
                     'Accession 2021-40-er has no risk csv. '],
                    ['rbrl003', '2024', 'closed', 0.001, 18, 0, 1, 7, 10, 'nan']]
        self.assertEqual(result, expected, "Problem with test for Russell data")


if __name__ == '__main__':
    unittest.main()
