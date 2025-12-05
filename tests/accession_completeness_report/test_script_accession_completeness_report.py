"""
Tests for the script accession_completeness_report.py, which tests each accession for if it contains the four
required elements: preservation log, full risk report, initial manifest, and a bag.
"""
from datetime import date
import os
import pandas as pd
import subprocess
import unittest


def csv_to_list(csv_path):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = pd.read_csv(csv_path)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the test output if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        for folder in ('complete', 'incomplete'):
            report_path = os.path.join('test_data', 'script', folder, f'accession_completeness_report_{today}.csv')
            if os.path.exists(report_path):
                os.remove(report_path)

    def test_complete(self):
        """Test for an input directory that contains only complete accessions, so no report is generated,
        as well as a folder at the status level that is not backlogged or closed and is skipped"""
        # Makes the variable used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'accession_completeness_report.py')
        input_directory = os.path.join('test_data', 'script', 'complete')
        script_message = subprocess.run(f'python {script} {input_directory}', shell=True, stdout=subprocess.PIPE)

        # Tests the correct message is printed.
        today = date.today().strftime('%Y-%m-%d')
        result = script_message.stdout.decode('utf-8')
        expected = (f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_1', 'acc_1_1')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_2', 'acc_2_1')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_2', 'acc_2_2')}\r\n"
                    f"\r\nAll accessions are complete.\r\n")
        self.assertEqual(expected, result, "Problem with test for complete, printed message")

        # Tests the csv was not made.
        result = os.path.exists(os.path.join(input_directory, f'accession_completeness_report_{today}.csv'))
        self.assertEqual(result, False, "Problem with test for complete, report")

    def test_incomplete(self):
        """Test for an input directory that contains some incomplete accessions, so the report is generated
        but also includes complete accessions and a collection from the unconventional collection list
        that will not be in the report"""
        # Makes the variable used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'accession_completeness_report.py')
        input_directory = os.path.join('test_data', 'script', 'incomplete')
        script_message = subprocess.run(f'python {script} {input_directory}', shell=True, stdout=subprocess.PIPE)

        # Tests the correct message is printed.
        today = date.today().strftime('%Y-%m-%d')
        report_path = os.path.join(input_directory, f'accession_completeness_report_{today}.csv')
        result = script_message.stdout.decode('utf-8')
        expected = (f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_1', 'acc_1_1')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_2', 'acc_2_1')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_2', 'acc_2_2')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'backlogged', 'coll_2', 'acc_2_3')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'closed', 'coll_3', 'acc_3_1')}\r\n"
                    f"Starting on accession {os.path.join(input_directory, 'closed', 'rbrl349', 'acc_349_1')}\r\n"
                    f"\r\nIncomplete accessions found. See {report_path}.\r\n")
        self.assertEqual(expected, result, "Problem with test for incomplete, printed message")

        # Tests the contents of the csv are correct.
        result = csv_to_list(report_path)
        expected = [['Status', 'Collection', 'Accession', 'Preservation_Log', 'Preservation_Log_Format',
                     'Full_Risk', 'Initial_Manifest', 'Bag'],
                    ['backlogged', 'coll_1', 'acc_1_1', False, 'Nonstandard columns', False, False, True],
                    ['backlogged', 'coll_2', 'acc_2_1', True, 'nan', True, False, False],
                    ['backlogged', 'coll_2', 'acc_2_3', False, 'nan', False, True, True],
                    ['closed', 'coll_3', 'acc_3_1', False, 'Extra blank row(s) at end', False, False, False],
                    ['closed', 'rbrl349', 'acc_349_1', True, 'nan', False, False, False]]
        self.assertEqual(expected, result, "Problem with test for incomplete, report")


if __name__ == '__main__':
    unittest.main()
