"""
Tests for the script collection_summary.py, which makes a CSV summarizing the collections in a directory.
"""
import unittest
import pandas as pd
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from subprocess import run


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete script output, if created"""
        today = datetime.today().strftime('%Y-%m-%d')
        reports = (join(getcwd(), '..', 'test_data', 'Hargrett_Hub', f"harg_hub-collection-summary_{today}.csv"),
                   join(getcwd(), '..', 'test_data', 'Russell_Hub', f"rbrl_hub-collection-summary_{today}.csv"))
        for report in reports:
            if exists(report):
                remove(report)

    def test_hargrett(self):
        """Test running the script with Hargrett test data"""
        directory = join(getcwd(), '..', 'test_data', 'Hargrett_Hub')
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        run(f'python {script} "{directory}"', shell=True)

        report = pd.read_csv(join(directory, f"harg_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"))
        result = [report.columns.tolist()] + report.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%'],
                    ['ms0001 Person papers', 2024, 'backlog', 0.00000001, 1, 100.0, 100.0, 100.0, 100.0],
                    ['ua01-001 Department records', 2024, 'backlog', 0.00000001, 1, 0.0, 0.0, 0.0, 100.0]]
        self.assertEqual(result, expected, "Problem with test for Hargrett data")

    def test_russell(self):
        """Test running the script with Russell test data"""
        directory = join(getcwd(), '..', 'test_data', 'Russell_Hub')
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        run(f'python {script} "{directory}"', shell=True)

        report = pd.read_csv(join(directory, f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"))
        result = [report.columns.tolist()] + report.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%'],
                    ['rbrl001', 2021, 'backlog', 0.00000001, 1, 100.0, 100.0, 100.0, 100.0],
                    ['rbrl002', 2022, 'backlog', 0.00000004, 4, 50.0, 75.0, 100.0, 150.0],
                    ['rbrl003', 2023, 'closed', 0.00000003, 3, 0.0, 0.0, 33.33, 100.0]]
        self.assertEqual(result, expected, "Problem with test for Russell data")


if __name__ == '__main__':
    unittest.main()
