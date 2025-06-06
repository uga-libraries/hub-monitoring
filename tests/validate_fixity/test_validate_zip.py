"""
Tests for the function validate_zip(), which validates a zipped accession using an MD5 from a text file
and returns information for the logs.
"""
import os
import unittest
from validate_fixity import validate_zip


class MyTestCase(unittest.TestCase):

    def test_not_valid(self):
        """Test for when the accession zip MD5 has changed"""
        # Makes the variables for the function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_zip', '2023-001-er')
        valid = validate_zip(accession_path)

        # Verifies the function returned the correct validation_result.
        expected = 'Fixity changed from 0000xxx000x0000x000xx0000xx00x00 to 6467ceb233d0519f561cd4367bd19e55.'
        self.assertEqual(valid, expected, 'Problem with test for not valid, validation_result')

    def test_valid(self):
        """Test for when the accession zip MD5 is still the same"""
        # Makes the variables for function input and runs the function.
        accession_path = os.path.join('test_data', 'validate_zip', '2023-002-er')
        valid = validate_zip(accession_path)

        # Verifies the function returned the correct validation_result.
        expected = 'Valid'
        self.assertEqual(valid, expected, 'Problem with test for valid, validation_result')


if __name__ == '__main__':
    unittest.main()
