"""
Tests for the function update_log(), which make a log of all accessions updated by the script.
"""
import unittest
from risk_update import update_log
from test_script_risk_update import csv_to_list
from os import getcwd, remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log, if it was made by a test."""
        log_path = join(getcwd(), 'update_risk_log.csv')
        if exists(log_path):
            remove(log_path)

    def test_existing_log(self):
        """Test for when there is already a log."""
        # Runs the function once to make a new log.
        parent_folder = join(getcwd(), 'dept', 'coll-001', 'acc-001')
        log_dir = getcwd()
        update_log(parent_folder, log_dir)

        # Runs the function again to add to an existing log.
        parent_folder = join(getcwd(), 'dept', 'coll-001', 'acc-002')
        log_dir = getcwd()
        update_log(parent_folder, log_dir)

        # Tests that the log was made.
        log_path = join(getcwd(), 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        result = csv_to_list(log_path)
        expected = [['Collection', 'Accession'], ['coll-001', 'acc-001'], ['coll-001', 'acc-002']]
        self.assertEqual(result, expected, "Problem with test for existing log, log contents")

    def test_new_log(self):
        """Test for when there is not already a log."""
        # Creates variables for function arguments and runs the function.
        parent_folder = join(getcwd(), 'coll-001', 'acc-001')
        log_dir = getcwd()
        update_log(parent_folder, log_dir)

        # Tests that the log was made.
        log_path = join(getcwd(), 'update_risk_log.csv')
        log_made = exists(log_path)
        self.assertEqual(log_made, True, "Problem with test for new log, log made")

        # Tests that the log has the expected contents.
        result = csv_to_list(log_path)
        expected = [['Collection', 'Accession'], ['coll-001', 'acc-001']]
        self.assertEqual(result, expected, "Problem with test for new log, log contents")


if __name__ == '__main__':
    unittest.main()
