"""
Tests for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import unittest
from collection_summary import get_accession_data
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_error_messages(self):
        """Test for when the accession has an error message from get_risk() and get_size()"""
        directory = join('test_data', 'Russell_Hub')
        status = 'closed'
        collection = 'rbrl003'
        accession = '2024-31-er'
        result = get_accession_data(directory, status, collection, accession)

        expected = ['2024-31-er', 'rbrl003', 'closed', '2024', 0, 0, 0, 0, 0, 0,
                    'Accession 2024-31-er has no risk csv. ',
                    'Could not calculate size for accession 2024-31-er due to folder organization. ']
        self.assertEqual(result, expected, "Problem with test for error messages")

    def test_no_error_messages(self):
        """Test for when the accession does not have any error messages."""
        directory = join('test_data', 'Hargrett_Hub')
        status = 'backlogged'
        collection = 'ms0001 Person papers'
        accession = '2022-15-er'
        result = get_accession_data(directory, status, collection, accession)

        expected = ['2022-15-er', 'ms0001 Person papers', 'backlogged', '2024', .00001, 3, 0, 0, 1, 2, '', None]
        self.assertEqual(result, expected, "Problem with test for no error messages")


if __name__ == '__main__':
    unittest.main()
