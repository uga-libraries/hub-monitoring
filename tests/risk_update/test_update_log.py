"""
Tests for the function update_log(), which make a log of all accessions updated by the script.
"""
import unittest
from risk_update import update_log
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv


def csv_to_list(csv_path):
    """Converts the contents of a csv to a list, with one item per row."""
    df = read_csv(csv_path)
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if it was made by a test."""
        log_path = join(getcwd(), 'update_risk_log.csv')
        if exists(log_path):
            remove(log_path)

    def test_existing_log(self):
        """Test for when there is already a log."""
        # Creates variables for function arguments.
        # Runs the function twice, first to make the log and then to add to the existing log.
        accession_path_1 = join(getcwd(), 'dept', 'coll-001', 'acc-001')
        accession_path_2 = join(getcwd(), 'dept', 'coll-001', 'acc-002')
        log_dir = getcwd()
        update_log(accession_path_1, log_dir)
        update_log(accession_path_2, log_dir)

        # Tests that the log was made.
        log_path = join(getcwd(), 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        log_contents = csv_to_list(log_path)
        expected = [['Collection', 'Accession'], ['coll-001', 'acc-001'], ['coll-001', 'acc-002']]
        self.assertEqual(log_contents, expected, "Problem with test for new log, log contents")

    def test_new_log(self):
        """Test for when there is not already a log."""
        # Creates variables for function arguments and runs the function.
        accession_path = join(getcwd(), 'coll-001', 'acc-001')
        log_dir = getcwd()
        update_log(accession_path, log_dir)

        # Tests that the log was made.
        log_path = join(getcwd(), 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        log_contents = csv_to_list(log_path)
        expected = [['Collection', 'Accession'], ['coll-001', 'acc-001']]
        self.assertEqual(log_contents, expected, "Problem with test for new log, log contents")


if __name__ == '__main__':
    unittest.main()
