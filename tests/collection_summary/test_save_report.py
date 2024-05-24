"""
Tests for the function save_report(), which saves the collection dataframe to a CSV.

Initially, the function calculated a different file name for the two departments.
The file name is now always the same, but the separate tests are retained in case we add department variation later,
since the tests already exist.
"""
import csv
import unittest
from collection_summary import save_report
from datetime import datetime
from os import remove
from os.path import exists, join
from pandas import DataFrame


def make_df(df_rows):
    """Make and return a dataframe with consistent column names."""
    column_names = ['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk', 'High_Risk',
                    'Moderate_Risk', 'Low_Risk', 'Notes']
    df = DataFrame(df_rows, columns=column_names)
    return df


def read_csv(csv_path):
    """Read CSV into a list, with one row per list.
    Would usually use pandas to read the CSV, but using csv library instead for a little more test independence."""
    with open(csv_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        row_list = list(reader)
    return row_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the reports, if they were made by the tests"""
        today = datetime.today().strftime('%Y-%m-%d')
        csv_paths = [join('test_data', 'Hargrett_Hub', f'hub-collection-summary_{today}.csv'),
                     join('test_data', 'Russell_Hub', f'hub-collection-summary_{today}.csv')]

        for path in csv_paths:
            if exists(path):
                remove(path)

    def test_harg(self):
        """Test for when the report should be saved in the Hargrett Hub"""
        # Makes test input and runs the function.
        rows = [['ms0001', 'backlog', 1.00, 111, '2015', 11, 15, 45, 40, ''],
                ['ms0002', 'backlog', 2.02, 200, '2019', 0, 0, 50, 150, ''],
                ['ms0003', 'backlog', 3.33, 303, '2021-2022', 100, 20, 33, 150, '']]
        coll_df = make_df(rows)
        directory = join('test_data', 'Hargrett_Hub')
        save_report(coll_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        csv_made = exists(csv_path)
        self.assertEqual(csv_made, True, "Problem with test for harg CSV is made")

        # Verifies the CSV has the expected contents.
        result = read_csv(csv_path)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['ms0001', 'backlog', '1.0', '111', '2015', '11', '15', '45', '40', ''],
                    ['ms0002', 'backlog', '2.02', '200', '2019', '0', '0', '50', '150', ''],
                    ['ms0003', 'backlog', '3.33', '303', '2021-2022', '100', '20', '33', '150', '']]
        self.assertEqual(result, expected, "Problem with test for harg CSV contents")

    def test_rbrl(self):
        """Test for when the report should be saved in the Russell Hub"""
        # Makes test input and runs the function.
        rows = [['rbrl001', 'backlog', 10.51, 852, '2015', 0, 0, 2, 850, ''],
                ['rbrl002', 'backlog', 20.20, 906, '2019', 100, 56, 212, 538, ''],
                ['rbrl003', 'backlog', 33.00, 1522, '2021-2022', 93, 942, 243, 244, '']]
        coll_df = make_df(rows)
        directory = join('test_data', 'Russell_Hub')
        save_report(coll_df, directory)

        # Verifies the expected CSV was made with the correct file name.
        csv_path = join(directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        csv_made = exists(csv_path)
        self.assertEqual(csv_made, True, "Problem with test for rbrl CSV is made")

        # Verifies the CSV has the expected contents.
        # Would usually use pandas to read the CSV, but using csv library instead for a little more test independence.
        result = read_csv(csv_path)
        expected = [['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['rbrl001', 'backlog', '10.51', '852', '2015', '0', '0', '2', '850', ''],
                    ['rbrl002', 'backlog', '20.2', '906', '2019', '100', '56', '212', '538', ''],
                    ['rbrl003', 'backlog', '33.0', '1522', '2021-2022', '93', '942', '243', '244', '']]
        self.assertEqual(result, expected, "Problem with test for rbrl CSV contents")


if __name__ == '__main__':
    unittest.main()
