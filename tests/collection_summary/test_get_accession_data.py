"""
Tests for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import os
import unittest
from collection_summary import get_accession_data


class MyTestCase(unittest.TestCase):

    def test_error_messages(self):
        """Test for when the accession has an error message from get_risk() and get_size()"""
        input_directory = os.path.join('test_data', 'Russell_Hub', 'born-digital')
        status = 'closed'
        collection = 'rbrl003'
        accession = '2024-31-er'
        accession_data = get_accession_data(input_directory, status, collection, accession)

        expected = ['2024-31-er', 'rbrl003', 'closed', '2024', 0, 0, 0, 0, 0, 0,
                    'Accession 2024-31-er has no risk csv. ', 'Accession bag not found. ']
        self.assertEqual(expected, accession_data, "Problem with test for error messages")

    def test_no_error_messages(self):
        """Test for when the accession does not have any error messages."""
        input_directory = os.path.join('test_data', 'Hargrett_Hub', 'Born-digital')
        status = 'backlogged'
        collection = 'ms0001 Person papers'
        accession = '2022-15-er'
        accession_data = get_accession_data(input_directory, status, collection, accession)

        expected = ['2022-15-er', 'ms0001 Person papers', 'backlogged', '2024', .00001, 3, 0, 0, 1, 2, None, None]
        self.assertEqual(expected, accession_data, "Problem with test for no error messages")


if __name__ == '__main__':
    unittest.main()
