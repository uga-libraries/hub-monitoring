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
        outputs = [join('test_data', 'Hargrett_Hub', f'hub-accession-summary_{today}.csv'),
                   join('test_data', 'Hargrett_Hub', f'hub-collection-summary_{today}.csv'),
                   join('test_data', 'Russell_Hub', f'hub-accession-summary_{today}.csv'),
                   join('test_data', 'Russell_Hub', f'hub-collection-summary_{today}.csv')]

        # Deletes any test output that is present.
        for output in outputs:
            if exists(output):
                remove(output)

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables needed for the script input.
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        input_directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(CalledProcessError):
            run(f'python "{script}" "{input_directory}"', shell=True, check=True, stdout=PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = run(f'python "{script}" "{input_directory}"', shell=True, stdout=PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided input_directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")

    def test_hargrett(self):
        """Test running the script with Hargrett test data"""
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        input_directory = join('test_data', 'Hargrett_Hub')
        run(f'python "{script}" "{input_directory}"', shell=True, stdout=PIPE)

        # Tests the contents of the accession report.
        acc_path = join(input_directory, f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(acc_path)
        expected = [['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['2022-15-er', 'ms0001 Person papers', 'backlogged', '2024', 0.00001, 3, 0, 0, 1, 2, 'nan', 'nan'],
                    ['ua_01_032_ER', 'ua01-001 Dept records', 'backlogged', '2024', 0.00000001, 1, 0, 0, 0, 1, 'nan', 'nan'],
                    ['ua_01_033_ER', 'ua01-001 Dept records', 'backlogged', '2024', 0.00004, 3, 1, 0, 1, 1, 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for Hargrett data, accession report")

        # Tests the contents of the collection report.
        coll_path = join(input_directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(coll_path)
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['ms0001 Person papers', '2024', 'backlogged', 0.00001, 3, 0, 0, 1, 2, 'nan', 'nan'],
                    ['ua01-001 Dept records', '2024', 'backlogged', 0.00004, 4, 1, 0, 1, 2, 'nan', 'nan']]
        self.assertEqual(result, expected, "Problem with test for Hargrett data, collection report")

    def test_russell(self):
        """Test running the script with Russell test data"""
        script = join(getcwd(), '..', '..', 'collection_summary.py')
        input_directory = join('test_data', 'Russell_Hub')
        run(f'python "{script}" "{input_directory}"', shell=True, stdout=PIPE)

        # Tests the contents of the accession report.
        acc_path = join(input_directory, f"hub-accession-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(acc_path)
        expected = [['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['2015-01-er', 'rbrl001', 'backlogged', '2024', 0.00005, 1, 0, 0, 0, 1, 'nan', 'nan'],
                    ['2015-12-er', 'rbrl001', 'backlogged', '2024', 0.00004, 1, 0, 0, 0, 1, 'nan', 'nan'],
                    ['2016-03-er', 'rbrl001', 'backlogged', '2024', 0.00005, 2, 0, 0, 0, 2, 'nan', 'nan'],
                    ['2018-04-er', 'rbrl001', 'backlogged', '2024', 0.0001, 5, 0, 0, 0, 5, 'nan', 'nan'],
                    ['2019-12-er', 'rbrl001', 'backlogged', '2024', 0.000001, 2, 0, 0, 0, 2, 'nan', 'nan'],
                    ['2021-11-er', 'rbrl002', 'backlogged', '2024', 0.00003, 4, 1, 0, 1, 2, 'nan', 'nan'],
                    ['2021-12-er', 'rbrl002', 'backlogged', '2024', 0.00003, 4, 2, 1, 2, 3, 'nan', 'nan'],
                    ['2021-13-er', 'rbrl002', 'backlogged', '2024', 0.00003, 4, 1, 1, 0, 2, 'nan', 'nan'],
                    ['2021-40-er', 'rbrl002', 'backlogged', '2024', 0.00003, 4, 0, 0, 0, 0,
                     'Accession 2021-40-er has no risk csv. ', 'nan'],
                    ['2022-01-er', 'rbrl002', 'backlogged', '2024', 0.00003, 4, 1, 1, 1, 1, 'nan', 'nan'],
                    ['2022-02-er', 'rbrl002', 'backlogged', '2024', 0.0001, 14, 5, 4, 3, 2, 'nan', 'nan'],
                    ['2022-03-er', 'rbrl002', 'backlogged', '2024', 0.00001, 1, 0, 0, 0, 1, 'nan', 'nan'],
                    ['2022-04-er', 'rbrl002', 'backlogged', '2024', 0.00001, 1, 0, 0, 1, 1, 'nan', 'nan'],
                    ['2022-05-er', 'rbrl002', 'backlogged', '2024', 0.00003, 5, 0, 2, 3, 0, 'nan', 'nan'],
                    ['2019-13-er', 'rbrl003', 'closed', '2024', 0.0002, 6, 0, 0, 0, 6, 'nan', 'nan'],
                    ['2022-27-er', 'rbrl003', 'closed', '2024', 0.00001, 1, 0, 0, 1, 0, 'nan', 'nan'],
                    ['2023-01-er', 'rbrl003', 'closed', '2024', 0.00001, 1, 0, 0, 1, 0, 'nan', 'nan'],
                    ['2023-12-er', 'rbrl003', 'closed', '2024', 0.0001, 2, 0, 0, 1, 1, 'nan', 'nan'],
                    ['2023-23-er', 'rbrl003', 'closed', '2024', 0.0005, 8, 0, 1, 4, 3, 'nan', 'nan'],
                    ['2024-31-er', 'rbrl003', 'closed', '2024', 0, 0, 0, 0, 0, 0,
                     'Accession 2024-31-er has no risk csv. ',
                     'Did not calculate size for accession 2024-31-er due to folder organization. ']]
        self.assertEqual(result, expected, "Problem with test for Russell data, accession report")

        # Tests the contents of the collection report.
        coll_path = join(input_directory, f"hub-collection-summary_{datetime.today().strftime('%Y-%m-%d')}.csv")
        result = csv_to_list(coll_path)
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['rbrl001', '2024', 'backlogged', 0.0002, 11, 0, 0, 0, 11, 'nan', 'nan'],
                    ['rbrl002', '2024', 'backlogged', 0.0003, 41, 10, 9, 11, 12,
                     'Accession 2021-40-er has no risk csv. ', 'nan'],
                    ['rbrl003', '2024', 'closed', 0, 0, 0, 1, 7, 10,
                     'Accession 2024-31-er has no risk csv. ',
                     'Did not calculate size for accession 2024-31-er due to folder organization. ']]
        self.assertEqual(result, expected, "Problem with test for Russell data, collection report")


if __name__ == '__main__':
    unittest.main()
