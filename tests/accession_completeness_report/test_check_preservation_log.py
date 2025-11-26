"""
Tests for the function check_preservation_log(), which checks the contents of the log are formatted correctly.
"""
import os
import unittest
from accession_completeness_report import check_preservation_log


class MyTestCase(unittest.TestCase):

    def test_correct(self):
        """Test for when the log is formatted correctly"""
        log_path = os.path.join('test_data', 'check_preservation_log', 'correct_preservation_log.txt')
        error = check_preservation_log(log_path)
        expected = None
        self.assertEqual(expected, error, "Problem with test for correct")

    def test_error_both(self):
        """Test for when the log has the wrong columns and an extra blank row at the end"""
        log_path = os.path.join('test_data', 'check_preservation_log', 'error_both_preservation_log.txt')
        error = check_preservation_log(log_path)
        expected = 'Nonstandard columns, Extra blank row(s) at end'
        self.assertEqual(expected, error, "Problem with test for error_both")

    def test_error_columns(self):
        """Test for when the log has the wrong columns"""
        log_path = os.path.join('test_data', 'check_preservation_log', 'error_columns_preservation_log.txt')
        error = check_preservation_log(log_path)
        expected = 'Nonstandard columns'
        self.assertEqual(expected, error, "Problem with test for error_columns")

    def test_error_row(self):
        """Test for when the log has extra blank rows at the end"""
        log_path = os.path.join('test_data', 'check_preservation_log', 'error_row_preservation_log.txt')
        error = check_preservation_log(log_path)
        expected = 'Extra blank row(s) at end'
        self.assertEqual(expected, error, "Problem with test for error_row")


if __name__ == '__main__':
    unittest.main()
