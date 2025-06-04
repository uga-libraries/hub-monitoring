"""
Tests for the function validate_zip(), which validates a zipped accession using an MD5 from a text file.
Updates the preservation log, and returns information for the validation log.
"""
from datetime import date
import os
import shutil
import unittest
from validate_fixity import validate_zip
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing."""
        accessions = [os.path.join('test_data', 'validate_zip', '2023-001-er'),
                      os.path.join('test_data', 'validate_zip', '2023-002-er')]
        for accession in accessions:
            shutil.copyfile(os.path.join(accession, 'preservation_log_copy.txt'),
                            os.path.join(accession, 'preservation_log.txt'))

    def test_not_valid(self):
        """Test for when the accession zip MD5 has changed"""
        # Makes the variables for the function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_zip', '2023-001-er')
        fixity = '2023-001-er_zip_md5.txt'
        valid = validate_zip(accession_path, fixity)

        # Verifies the function returned the correct validation_result.
        expected = 'Fixity changed from 0000xxx000x0000x000xx0000xx00x00 to 6467ceb233d0519f561cd4367bd19e55.'
        self.assertEqual(valid, expected, 'Problem with test for not valid, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(os.path.join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.1.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T4', '2023.1.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T4', '2023.1.ER', '2023-10-03', 'BLANK', 'Can\'t bag; zip and save MD5.', 'JD'],
                    ['T4', '2023.1.ER', '2023-10-03', 'BLANK', 'Validated zip MD5. Valid.', 'JD'],
                    ['T4', '2023.1.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated zip md5 for accession 2023.1.ER. The zip is not valid. '
                     'Fixity changed from 0000xxx000x0000x000xx0000xx00x00 to 6467ceb233d0519f561cd4367bd19e55.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for not valid, preservation_log.txt')

    def test_valid(self):
        """Test for when the accession zip MD5 is still the same"""
        # Makes the variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_zip', '2023-002-er')
        fixity = '2023-002-er_zip_md5.txt'
        valid = validate_zip(accession_path, fixity)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(valid, expected, 'Problem with test for valid, validation_result')

        # Verifies the preservation_log.txt has been updated correctly.
        result = csv_to_list(os.path.join(accession_path, 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.2.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.2.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.2.ER', '2023-10-03', 'BLANK', 'Can\'t bag; zip and save MD5.', 'JD'],
                    ['T5', '2023.2.ER', '2023-10-03', 'BLANK', 'Validated zip MD5. Valid.', 'JD'],
                    ['T5', '2023.2.ER', date.today().strftime('%Y-%m-%d'), 'BLANK',
                     'Validated zip md5 for accession 2023.2.ER. The zip md5 is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, preservation_log.txt')


if __name__ == '__main__':
    unittest.main()
