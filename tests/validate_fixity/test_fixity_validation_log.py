"""
Test for the function fixity_validation_log(), which makes a log with all accessions to be validated.
"""
from datetime import date
import os
import unittest
from validate_fixity import fixity_validation_log
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        log_path = os.path.join('test_data', 'fixity_validation_log',
                                f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
        if os.path.exists(log_path):
            os.remove(log_path)

    def test_function(self):
        # Makes the variable for function input and runs the function.
        input_directory = os.path.join('test_data', 'fixity_validation_log')
        fixity_validation_log(input_directory)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join('test_data', 'fixity_validation_log',
                                          f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Fixity_Type', 'Validation_Result'],
                    ['backlogged', 'coll_1', 'acc_1_1_er', 'Bag', 'nan'],
                    ['backlogged', 'coll_1', 'acc_1_2_ER', 'Bag', 'nan'],
                    ['backlogged', 'coll_2', 'acc_2-1-er', 'InitialManifest', 'nan'],
                    ['backlogged', 'coll_2', 'acc_2-2-ER', 'InitialManifest', 'nan'],
                    ['closed', 'coll_3', 'no-acc-num', 'Bag', 'nan']]
        self.assertEqual(result, expected, "Problem with test for fixity_validation_log function")


if __name__ == '__main__':
    unittest.main()
