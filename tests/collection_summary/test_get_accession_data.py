"""
Test for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import unittest
from collection_summary import get_accession_data
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        directory = join('test_data', 'Hargrett_Hub')
        status = 'backlogged'
        collection = 'ms0001 Person papers'
        accession = '2022-15-er'
        result = get_accession_data(directory, status, collection, accession)

        expected = ['2022-15-er', 'ms0001 Person papers', 'backlogged', '2024', .00001, 3, 0, 0, 1, 2, '', None]
        self.assertEqual(result, expected, "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
