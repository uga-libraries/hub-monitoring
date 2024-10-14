"""
Tests for the function update_log(), which make a log of all accessions updated by the script.
"""
import unittest
from risk_update import update_log
from test_script_risk_update import csv_to_list
from datetime import datetime
from os import getcwd, remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        today = datetime.today().strftime('%Y-%m-%d')
        if exists(f"update_risk_log_{today}.csv"):
            remove(f"update_risk_log_{today}.csv")

    def test_existing_log(self):
        """Test for when there is already a log."""
        # Runs the function once to make a new log.
        root = join(getcwd(), 'dept', 'coll-001', 'acc-001')
        input_directory = getcwd()
        update_log(root, input_directory, 'Yes')

        # Runs the function again to add to an existing log.
        root = join(getcwd(), 'dept', 'coll-001', 'acc-002')
        input_directory = getcwd()
        update_log(root, input_directory, 'Yes')

        # Tests that the log was made.
        today = datetime.today().strftime('%Y-%m-%d')
        log_path = join(getcwd(), f"update_risk_log_{today}.csv")
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        result = csv_to_list(log_path)
        expected = [['Collection', 'Accession', 'Risk_Updated'],
                    ['coll-001', 'acc-001', 'Yes'],
                    ['coll-001', 'acc-002', 'Yes']]
        self.assertEqual(result, expected, "Problem with test for existing log, log contents")

    def test_new_log(self):
        """Test for when there is not already a log."""
        # Creates variables for function arguments and runs the function.
        root = join(getcwd(), 'coll-001', 'acc-001')
        input_directory = getcwd()
        update_log(root, input_directory, 'No')

        # Tests that the log was made.
        today = datetime.today().strftime('%Y-%m-%d')
        log_path = join(getcwd(), f"update_risk_log_{today}.csv")
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        result = csv_to_list(log_path)
        expected = [['Collection', 'Accession', 'Risk_Updated'], ['coll-001', 'acc-001', 'No']]
        self.assertEqual(result, expected, "Problem with test for new log, log contents")


if __name__ == '__main__':
    unittest.main()
