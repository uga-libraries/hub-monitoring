"""
Tests for the function update_fixity_validation_log(), which adds the validation result to the log.
To simplify the tests, information in the logs is abbreviated and may not align with the validation result supplied.

Note: the result includes a timestamp to a minute, so if that fails, check if it is just off by minute.
That could mean it is working fine but the clock ticked over 1 minute between making the output and testing it.
"""
from datetime import datetime
import os
import pandas as pd
import unittest
from validate_fixity import update_fixity_validation_log
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Make the dataframe and csv of the log that the tests will update"""
        row_list = [['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag', None, None, None],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt', None, None, None]]
        columns_list = ['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                        'Valid', 'Valid_Time', 'Result']
        self.log_df = pd.DataFrame(row_list, columns=columns_list)
        self.log_df.to_csv('fixity_validation_20241031.csv', index=False)

    def tearDown(self):
        """Delete the test output if it was created"""
        if os.path.exists('fixity_validation_20241031.csv'):
            os.remove('fixity_validation_20241031.csv')

    def test_one_change(self):
        """Test for adding the validation result to one row and result is "Valid"."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Valid')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'BLANK', 'BLANK', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for one change to the log")

    def test_two_changes(self):
        """Test for adding the validation result to two rows and result is "Valid"."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Valid')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, 'Valid')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid']]
        self.assertEqual(result, expected, "Problem with test for two changes to the log")

    def test_not_valid_bag(self):
        """Test for adding the validation result when result is a bag validation error."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Payload-Oxum failed.')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, 'Bag validation failed.')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Payload-Oxum failed.'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Bag validation failed.']]
        self.assertEqual(result, expected, "Problem with test for not valid, bag error")

    def test_not_valid_bag_manifest(self):
        """Test for adding the validation result when result is "# bag manifest errors"."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, '1 bag manifest errors.')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, '99 bag manifest errors.')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), '1 bag manifest errors.'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), '99 bag manifest errors.']]
        self.assertEqual(result, expected, "Problem with test for not valid, bag manifest")

    def test_not_valid_fixity_changed(self):
        """Test for adding the validation result when result is "Fixity changed from..."."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Fixity changed from x to y.')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, 'Fixity changed from x to y.')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Fixity changed from x to y.'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'False', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Fixity changed from x to y.']]
        self.assertEqual(result, expected, "Problem with test for not valid, fixity changed")

    def test_valid_bag_manifest(self):
        """Test for adding the validation result when result is "Valid (bag manifest)"."""
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 0, 'Valid (bag manifest)')
        update_fixity_validation_log('fixity_validation_20241031.csv', self.log_df, 1, 'Valid (bag manifest)')

        # Verifies the fixity validation log CSV has the correct values.
        result = csv_to_list('fixity_validation_20241031.csv')
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity',
                     'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'c1', 'a1-er', 'path\\a1-er', 'Bag', 'a1-er_bag',
                     'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid (bag manifest)'],
                    ['closed', 'c1', 'a2-er', 'path\\a2-er', 'Zip', 'a2-er_zip_md5.txt',
                     'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid (bag manifest)']]
        self.assertEqual(result, expected, "Problem with test for valid bag manifest")


if __name__ == '__main__':
    unittest.main()
