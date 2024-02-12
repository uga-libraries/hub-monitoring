"""
Test for the function save_report(), which saves the collection dataframe to a CSV.
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
        csv_name = f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv"
        csv_path = join(getcwd(), '..', 'test_data', csv_name)
        if exists(csv_path):
            remove(csv_path)

    def test_function(self):
        # Makes test input and runs the function.
        collection_df = DataFrame([['c1', 'backlog', 10, 111, '2015', 0.0, 3.0, 17.5, 79.5],
                                   ['c2', 'backlog', 20, 200, '2019', 10.0, 3.9, 42.1, 44.0],
                                   ['c3', 'backlog', 33, 303, '2021-2022', 90.0, 0.0, 0.0, 10.0]],
                                  columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%',
                                           'High_Risk_%', 'Moderate_Risk_%', 'Low_Risk_%'])
        directory = join(getcwd(), '..', 'test_data')
        save_report(collection_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"rbrl_hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = exists(csv_path)
        self.assertEqual(result, True, "Problem with test for CSV is made")

        # Verifies the CSV has the expected contents.
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            result = list(reader)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk_%', 'High_Risk_%',
                     'Moderate_Risk_%', 'Low_Risk_%'],
                    ['c1', 'backlog', '10', '111', '2015', '0.0', '3.0', '17.5', '79.5'],
                    ['c2', 'backlog', '20', '200', '2019', '10.0', '3.9', '42.1', '44.0'],
                    ['c3', 'backlog', '33', '303', '2021-2022', '90.0', '0.0', '0.0', '10.0']]
        self.assertEqual(result, expected, "Problem with test for CSV contents")


if __name__ == '__main__':
    unittest.main()
