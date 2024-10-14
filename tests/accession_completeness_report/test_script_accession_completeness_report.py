"""
Tests for the script accession_completeness_report.py, which tests each accession for if it contains the four
required elements: preservation log, full risk report, initial manifest, and a bag.
"""
import subprocess
import unittest
from datetime import date
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv


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
        """Deletes the test output if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('script_test_data', 'incomplete', f'accession_completeness_report_{today}.csv')):
            remove(join('script_test_data', 'incomplete', f'accession_completeness_report_{today}.csv'))

    def test_complete(self):
        """Test for an input directory that contains only complete accessions, so no report is generated,
        as well as a folder at the status level that is not backlogged or closed and is skipped"""
        # Makes the variable used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'accession_completeness_report.py')
        input_directory = join('script_test_data', 'complete')
        script_message = subprocess.run(f'python {script} {input_directory}', shell=True, stdout=subprocess.PIPE)

        # Tests the correct message is printed.
        today = date.today().strftime('%Y-%m-%d')
        result = script_message.stdout.decode('utf-8')
        expected = (f"Starting on accession {join(input_directory, 'backlogged', 'coll_1', 'acc_1_1')}\r\n"
                    f"Starting on accession {join(input_directory, 'backlogged', 'coll_2', 'acc_2_1')}\r\n"
                    f"Starting on accession {join(input_directory, 'backlogged', 'coll_2', 'acc_2_2')}\r\n"
                    f"\r\nAll accessions are complete.\r\n")
        self.assertEqual(result, expected, "Problem with test for complete, printed message")

        # Tests the csv was not made.
        result = exists(join(input_directory, f'accession_completeness_report_{today}.csv'))
        self.assertEqual(result, False, "Problem with test for complete, report")

    def test_incomplete(self):
        """Test for an input directory that contains some incomplete accessions, so the report is generated
        but also includes complete accessions and a collection from the unconventional collection list
        that will not be in the report"""
        # Makes the variable used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'accession_completeness_report.py')
        input_directory = join('script_test_data', 'incomplete')
        script_message = subprocess.run(f'python {script} {input_directory}', shell=True, stdout=subprocess.PIPE)

        # Tests the correct message is printed.
        today = date.today().strftime('%Y-%m-%d')
        report_path = join(input_directory, f'accession_completeness_report_{today}.csv')
        result = script_message.stdout.decode('utf-8')
        expected = (f"Starting on accession {join(input_directory, 'backlogged', 'coll_1', 'acc_1_1')}\r\n"
                    f"Starting on accession {join(input_directory, 'backlogged', 'coll_2', 'acc_2_1')}\r\n"
                    f"Starting on accession {join(input_directory, 'backlogged', 'coll_2', 'acc_2_2')}\r\n"
                    f"Starting on accession {join(input_directory, 'backlogged', 'coll_2', 'acc_2_3')}\r\n"
                    f"Starting on accession {join(input_directory, 'closed', 'coll_3', 'acc_3_1')}\r\n"
                    f"\r\nIncomplete accessions found. See {report_path}.\r\n")
        self.assertEqual(result, expected, "Problem with test for incomplete, printed message")

        # Tests the contents of the csv are correct.
        result = csv_to_list(report_path)
        expected = [['Status', 'Collection', 'Accession', 'Preservation_Log', 'Full_Risk', 'Initial_Manifest', 'Bag'],
                    ['backlogged', 'coll_1', 'acc_1_1', True, False, False, True],
                    ['backlogged', 'coll_2', 'acc_2_1', True, True, False, False],
                    ['backlogged', 'coll_2', 'acc_2_3', False, False, True, True],
                    ['closed', 'coll_3', 'acc_3_1', True, False, False, False]]
        self.assertEqual(result, expected, "Problem with test for incomplete, report")


if __name__ == '__main__':
    unittest.main()
