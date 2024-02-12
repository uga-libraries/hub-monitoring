"""
Tests for the function save_report(), which saves the collection dataframe to a CSV.
"""
import csv
import unittest
from collection_summary import save_report
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the reports, if they were made by the tests"""
        base_name = f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"
        csv_paths = [join(getcwd(), '..', 'test_data', 'Hargrett_Hub', f'harg_{base_name}'),
                     join(getcwd(), '..', 'test_data', 'Russell_Hub', f'rbrl_{base_name}')]

        for path in csv_paths:
            if exists(path):
                remove(path)

    def test_harg(self):
        """Test for when the report should be saved with a harg prefix"""
        # Makes test input and runs the function.
        collection_df = DataFrame([['ms0001', 'backlog', 1, 111, '2015', 0.0, 3.0, 17.5, 79.5],
                                   ['ms0002', 'backlog', 2, 200, '2019', 10.0, 3.9, 42.1, 44.0],
                                   ['ms0003', 'backlog', 3, 303, '2021-2022', 90.0, 0.0, 0.0, 10.0]],
                                  columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%',
                                           'High_Risk_%', 'Moderate_Risk_%', 'Low_Risk_%'])
        directory = join(getcwd(), '..', 'test_data', 'Hargrett_Hub')
        save_report(collection_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"harg_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = exists(csv_path)
        self.assertEqual(result, True, "Problem with test for harg CSV is made")

        # Verifies the CSV has the expected contents.
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            result = list(reader)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%'],
                    ['ms0001', 'backlog', '1', '111', '2015', '0.0', '3.0', '17.5', '79.5'],
                    ['ms0002', 'backlog', '2', '200', '2019', '10.0', '3.9', '42.1', '44.0'],
                    ['ms0003', 'backlog', '3', '303', '2021-2022', '90.0', '0.0', '0.0', '10.0']]
        self.assertEqual(result, expected, "Problem with test for harg CSV contents")

    def test_rbrl(self):
        """Test for when the report should be saved with a rbrl prefix"""
        # Makes test input and runs the function.
        collection_df = DataFrame([['rbrl001', 'backlog', 10, 111, '2015', 0.0, 3.0, 17.5, 79.5],
                                   ['rbrl002', 'backlog', 20, 200, '2019', 10.0, 3.9, 42.1, 44.0],
                                   ['rbrl003', 'backlog', 33, 303, '2021-2022', 90.0, 0.0, 0.0, 10.0]],
                                  columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%',
                                           'High_Risk_%', 'Moderate_Risk_%', 'Low_Risk_%'])
        directory = join(getcwd(), '..', 'test_data', 'Russell_Hub')
        save_report(collection_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = exists(csv_path)
        self.assertEqual(result, True, "Problem with test for rbrl CSV is made")

        # Verifies the CSV has the expected contents.
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            result = list(reader)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%'],
                    ['rbrl001', 'backlog', '10', '111', '2015', '0.0', '3.0', '17.5', '79.5'],
                    ['rbrl002', 'backlog', '20', '200', '2019', '10.0', '3.9', '42.1', '44.0'],
                    ['rbrl003', 'backlog', '33', '303', '2021-2022', '90.0', '0.0', '0.0', '10.0']]
        self.assertEqual(result, expected, "Problem with test for rbrl CSV contents")


if __name__ == '__main__':
    unittest.main()
