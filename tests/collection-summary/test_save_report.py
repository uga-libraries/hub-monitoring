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
        collection_df = DataFrame([['ms0001', 'backlog', 1.00, 111, '2015', 47.75, 15.32, 0.00, 36.94],
                                   ['ms0002', 'backlog', 2.02, 200, '2019', 10.00, 0.00, 50.00, 40.00],
                                   ['ms0003', 'backlog', 3.33, 303, '2021-2022', 33.00, 0.99, 4.95, 61.06]],
                                  columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%',
                                           'High_Risk_%', 'Moderate_Risk_%', 'Low_Risk_%'])
        directory = join(getcwd(), '..', 'test_data', 'Hargrett_Hub')
        save_report(collection_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"harg_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = exists(csv_path)
        self.assertEqual(result, True, "Problem with test for harg CSV is made")

        # Verifies the CSV has the expected contents.
        # Would usually use pandas to read the CSV, but using csv library instead for a little more test independence.
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            result = list(reader)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%', 'Notes'],
                    ['ms0001', 'backlog', '1.0', '111', '2015', '47.75', '15.32', '0.0', '36.94', ''],
                    ['ms0002', 'backlog', '2.02', '200', '2019', '10.0', '0.0', '50.0', '40.0', ''],
                    ['ms0003', 'backlog', '3.33', '303', '2021-2022', '33.0', '0.99', '4.95', '61.06', '']]
        self.assertEqual(result, expected, "Problem with test for harg CSV contents")

    def test_rbrl(self):
        """Test for when the report should be saved with a rbrl prefix"""
        # Makes test input and runs the function.
        collection_df = DataFrame([['rbrl001', 'backlog', 10.51, 852, '2015', 0.00, 0.00, 0.00, 100.00],
                                   ['rbrl002', 'backlog', 20.20, 906, '2019', 40.40, 4.42, 55.19, 0.00],
                                   ['rbrl003', 'backlog', 33.00, 1522, '2021-2022', 5.91, 11.83, 3.29, 78.98]],
                                  columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%',
                                           'High_Risk_%', 'Moderate_Risk_%', 'Low_Risk_%'])
        directory = join(getcwd(), '..', 'test_data', 'Russell_Hub')
        save_report(collection_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = exists(csv_path)
        self.assertEqual(result, True, "Problem with test for rbrl CSV is made")

        # Verifies the CSV has the expected contents.
        # Would usually use pandas to read the CSV, but using csv library instead for a little more test independence.
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            result = list(reader)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%', 'Notes'],
                    ['rbrl001', 'backlog', '10.51', '852', '2015', '0.0', '0.0', '0.0', '100.0', ''],
                    ['rbrl002', 'backlog', '20.2', '906', '2019', '40.4', '4.42', '55.19', '0.0', ''],
                    ['rbrl003', 'backlog', '33.0', '1522', '2021-2022', '5.91', '11.83', '3.29', '78.98', '']]
        self.assertEqual(result, expected, "Problem with test for rbrl CSV contents")


if __name__ == '__main__':
    unittest.main()
