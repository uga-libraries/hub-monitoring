"""
Tests for the script collection_summary.py, which makes a CSV summarizing the collections in a directory.
"""
import unittest
import pandas as pd
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from subprocess import CalledProcessError, PIPE, run


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete script output, if created"""
        today = datetime.today().strftime('%Y-%m-%d')
        reports = (join(getcwd(), '..', 'test_data', 'Hargrett_Hub', f"harg_hub-collection-summary_{today}.csv"),
                   join(getcwd(), '..', 'test_data', 'Russell_Hub', f"rbrl_hub-collection-summary_{today}.csv"))
        for report in reports:
            if exists(report):
                remove(report)

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables needed for the script input.
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(CalledProcessError):
            run(f'python {script} {directory}', shell=True, check=True, stdout=PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = run(f'python {script} {directory}', shell=True, stdout=PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")

    def test_hargrett(self):
        """Test running the script with Hargrett test data"""
        directory = join(getcwd(), '..', 'test_data', 'Hargrett_Hub')
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        run(f'python {script} "{directory}"', shell=True)

        report = pd.read_csv(join(directory, f"harg_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"),
                             dtype={'Date': str})
        report = report.fillna('nan')
        result = [report.columns.tolist()] + report.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%', 'Notes'],
                    ['ms0001 Person papers', '2024', 'backlog', 0.00001, 3, 0.0, 0.0, 33.33, 66.67, 'nan'],
                    ['ua01-001 Dept records', '2024', 'backlog', 0.00004, 4, 25.0, 0.0, 25.0, 50.0, 'nan']]
        self.assertEqual(result, expected, "Problem with test for Hargrett data")

    def test_russell(self):
        """Test running the script with Russell test data"""
        directory = join(getcwd(), '..', 'test_data', 'Russell_Hub')
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        run(f'python {script} "{directory}"', shell=True, stdout=PIPE)

        report = pd.read_csv(join(directory, f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"),
                             dtype={'Date': str})
        report = report.fillna('nan')
        result = [report.columns.tolist()] + report.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%', 'Notes'],
                    ['rbrl001', '2024', 'backlog', 0.0002, 11, 0.0, 0.0, 0.0, 100.0, 'nan'],
                    ['rbrl002', '2024', 'backlog', 0.0003, 41, 24.39, 21.95, 26.83, 29.27, 'nan'],
                    ['rbrl003', '2024', 'closed', 0.001, 18, 0.0, 5.56, 38.89, 55.56, 'nan']]
        self.assertEqual(result, expected, "Problem with test for Russell data")


if __name__ == '__main__':
    unittest.main()
