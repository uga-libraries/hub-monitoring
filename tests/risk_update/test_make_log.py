"""
Test for the function make_log(), which makes a log with all accessions to be updated.
"""
from datetime import date
import os
import unittest
from risk_update import make_log
from test_script_risk_update import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the log if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        log_path = os.path.join('test_data', 'make_log', f'risk_update_log_{today}.csv')
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_function(self):
        # Makes the variable for the function input and runs the function.
        input_directory = os.path.join('test_data', 'make_log')
        make_log(input_directory)

        # Verifies the log has the correct values.
        today = date.today().strftime('%Y-%m-%d')
        result = csv_to_list(os.path.join('test_data', 'make_log', f'risk_update_log_{today}.csv'))
        expected = [['Collection', 'Accession', 'Accession_Path', 'Risk_Updated'],
                    ['coll1', 'acc-1-er', os.path.join('test_data', 'make_log', 'coll1', 'acc-1-er'), 'nan'],
                    ['coll1', 'acc-2-ER', os.path.join('test_data', 'make_log', 'coll1', 'acc-2-ER'), 'nan'],
                    ['coll1', 'acc-3_ER', os.path.join('test_data', 'make_log', 'coll1', 'acc-3_ER'), 'nan'],
                    ['coll2', 'acc-4_er', os.path.join('test_data', 'make_log', 'coll2', 'acc-4_er'), 'nan'],
                    ['coll2', 'no-acc-num', os.path.join('test_data', 'make_log', 'coll2', 'no-acc-num'), 'nan']]
        self.assertEqual(result, expected, "Problem wit test for make_log function")


if __name__ == '__main__':
    unittest.main()
