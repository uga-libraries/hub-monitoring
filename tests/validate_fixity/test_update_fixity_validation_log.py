"""
Tests for the function update_fixity_validation_log(), which adds the validation result to the log.
To simplify the tests, information in the logs is abbreviated.
"""
import os
import pandas as pd
import unittest
from validate_fixity import update_fixity_validation_log
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Make the dataframe and csv of the log that the tests will update"""
        row_list = [['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag', None, None],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'InitialManifest', None, 'initialmanifest.csv', None]]
        columns_list = ['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type',
                        'Bag_Name', 'Manifest_Name', 'Validation_Result']
        self.log_df = pd.DataFrame(row_list, columns=columns_list)
        self.log_df.to_csv('fixity_validation_20241031.csv', index=False)

    def tearDown(self):
        """Delete the test output if it was created"""
        if os.path.exists('fixity_validation_20241031.csv'):
            os.remove('fixity_validation_20241031.csv')

    def test_one_change(self):
        """Test for adding the validation result to one row."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Valid')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type',
                     'Bag_Name', 'Manifest_Name', 'Validation_Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag', 'nan', 'Valid'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'InitialManifest', 'nan', 'initialmanifest.csv', 'nan']]
        self.assertEqual(result, expected, "Problem with tst for one change to the log")

    def test_two_changes(self):
        """Test for adding the validation result to two rows."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Not valid')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, 'Valid')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type',
                     'Bag_Name', 'Manifest_Name', 'Validation_Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag', 'nan', 'Not valid'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'InitialManifest', 'nan', 'initialmanifest.csv', 'Valid']]
        self.assertEqual(result, expected, "Problem with tst for two changes to the log")


if __name__ == '__main__':
    unittest.main()
