"""
Tests for the function update_log(), which adds the result of updating an accession to the log.
To simplify the tests, information in the logs is abbreviated.
"""
import os
import pandas as pd
import unittest
from risk_update import update_log
from test_script_risk_update import csv_to_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Make the dataframe and csv of the log that the tests will update"""
        row_list = [['c1', 'a1', 'path\\c1\\a1', None],
                    ['c1', 'a2', 'path\\c1\\a2', None],
                    ['c2', 'a3', 'path\\c2\\a3', None]]
        columns_list = ['Collection', 'Accession', 'Accession_Path', 'Risk_Updated']
        self.log_df = pd.DataFrame(row_list, columns=columns_list)
        self.log_df.to_csv('risk_update_log_2024-1101.csv')

    def tearDown(self):
        """Delete the log, which is edited by the test, so it can be remade"""
        if os.path.exists('risk_update_log_2024-1101.csv'):
            os.remove('risk_update_log_2024-1101.csv')

    def test_one_change(self):
        """Test for adding the risk update result to one row."""
        update_log('risk_update_log_2024-1101.csv', self.log_df, 0, 'Yes')

        # Verifies the risk update log has the correct values.
        result = csv_to_list('risk_update_log_2024-1101.csv')
        expected = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                    ['c1', 'a1', 'path\\c1\\a1', 'Yes'],
                    ['c1', 'a2', 'path\\c1\\a2', 'nan'],
                    ['c2', 'a3', 'path\\c2\\a3', 'nan']]
        self.assertEqual(result, expected, "Problem with test for one change to the log")

    def test_two_changes(self):
        """Test for adding the risk update result to two rows."""
        update_log('risk_update_log_2024-1101.csv', self.log_df, 0, 'No')
        update_log('risk_update_log_2024-1101.csv', self.log_df, 1, 'Yes')

        # Verifies the risk update log has the correct values.
        result = csv_to_list('risk_update_log_2024-1101.csv')
        expected = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                    ['c1', 'a1', 'path\\c1\\a1', 'No'],
                    ['c1', 'a2', 'path\\c1\\a2', 'Yes'],
                    ['c2', 'a3', 'path\\c2\\a3', 'nan']]
        self.assertEqual(result, expected, "Problem with test for two changes to the log")


if __name__ == '__main__':
    unittest.main()
