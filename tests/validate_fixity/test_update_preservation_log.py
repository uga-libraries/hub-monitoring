"""
Tests for the function log_status = update_preservation_log(), which adds validation information to an accession's preservation log.
"""
from datetime import date
import os
import shutil
import unittest
from validate_fixity import update_preservation_log
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder"""
        accessions = ['2023_1_er', '2023_2_er', '2023_3_er', '2023_4_er', '2023_5_er', '2023_6_er',
                      '2023_8_er']
        for accession in accessions:
            accession_path = os.path.join('test_data', 'update_preservation_log', accession)
            shutil.copyfile(os.path.join(accession_path, 'preservation_log_copy.txt'),
                            os.path.join(accession_path, 'preservation_log.txt'))

    def test_bag_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_1_er')
        validation_result = 'Payload-Oxum validation failed. Expected 2 files but found 3 files'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for bag not valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.1.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.1.ER', '2023-02-28', 'BLANK', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.1.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated bag for accession 2023.1.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 2 files but found 3 files', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for bag not valid, log contents')

    def test_bag_valid(self):
        """Test for when the bag is valid"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_2_er')
        validation_result = 'Valid'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for bag valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.2.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.2.ER', '2023-02-28', 'BLANK', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.2.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated bag for accession 2023.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for bag valid, log contents')

    def test_bag_manifest_not_valid(self):
        """Test for when the bag cannot be validated with bagit and bag manifest is not valid"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_3_er')
        validation_result = 'Could not validate with bagit. Bag manifest not valid: 12 errors'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for bag manifest not valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.ER', '2023-02-28', 'BLANK', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated bag for accession 2023.3.ER. The bag is not valid. Could not validate with bagit. '
                     'Bag manifest not valid: 12 errors', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for bag manifest not valid, log contents')

    def test_bag_manifest_valid(self):
        """Test for when the bag cannot be validated with bagit and the bag manifest is valid"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_4_er')
        validation_result = 'Valid (bag manifest - could not validate with bagit'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for bag manifest valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.4.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.4.ER', '2023-02-28', 'BLANK', 'Bagged accession, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.4.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated bag for accession 2023.4.ER. '
                     'Valid (bag manifest - could not validate with bagit', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for bag manifest valid, log contents')

    def test_zip_not_valid(self):
        """Test for when the MD5 for the zip is not valid (is changed)"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_5_er')
        validation_result = 'Fixity changed from xxxxxxxxx to yyyyyyyyy.'
        fixity_type = 'Zip'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for zip not valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.5.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.5.ER', '2023-02-28', 'BLANK', 'Made zip, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.5.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated zip md5 for accession 2023.5.ER. The zip is not valid. '
                     'Fixity changed from xxxxxxxxx to yyyyyyyyy.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for zip not valid, log contents')

    def test_zip_valid(self):
        """Test for when the MD5 for the zip is valid (has not changed)"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_6_er')
        validation_result = 'Valid'
        fixity_type = 'Zip'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for zip valid, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.6.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.6.ER', '2023-02-28', 'BLANK', 'Made zip, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.6.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated zip for accession 2023.6.ER. The zip is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for zip valid, log contents')

    def test_error_no_end_return(self):
        """Test for when the preservation_log.txt has no return at the end of the last line"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_8_er')
        validation_result = 'Valid'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Updated', log_status, 'Problem with test for error - no end return, log_status')

        # Verifies the contents of the log have been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.7.ER', '2023-02-28', 'CD1', 'Copied, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.7.ER', '2023-02-28', 'BLANK', 'Made bag, no errors.', 'Jane Doe'],
                    ['TEST.3', '2023.7.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated bag for accession 2023.7.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for error - no end return, log_status')

    def test_error_no_log(self):
        """Test for when there is no preservation log to update"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_9_er')
        validation_result = 'Valid'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Log path not found', log_status, 'Problem with test for error - no log, log_status')

    def test_error_nonstandard(self):
        """Test for when the preservation_log.txt does not have the standard columns"""
        # Makes the variables needed for function input and runs the function.
        acc_dir = os.path.join('test_data', 'update_preservation_log', '2023_10_er')
        validation_result = 'Valid'
        fixity_type = 'Bag'
        log_status = update_preservation_log(acc_dir, validation_result, fixity_type)

        # Verifies the function returned the correct log_status.
        self.assertEqual('Nonstandard columns', log_status, 'Problem with test for nonstandard, log_status')

        # Verifies the contents of the log have NOT been updated.
        result = csv_to_list(os.path.join(acc_dir, 'preservation_log.txt'), delimiter='\t')
        expected = [['Date', 'Electronic Media Identifier', 'Action', 'Staff'],
                    ['2023-02-28', 'Test003.008.CD1', 'Copied, no errors.', 'Jane Doe']]
        self.assertEqual(expected, result, 'Problem with test for error - nonstandard, log contents')




if __name__ == '__main__':
    unittest.main()
