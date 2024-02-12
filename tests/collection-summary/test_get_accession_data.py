"""
Test for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import unittest
from collection_summary import get_accession_data
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        directory = join(getcwd(), '..', 'test_data', 'Russell_Hub')
        accession_list = get_accession_data(directory, 'backlog', 'rbrl002', '2022-01-er')
        accession_list_expected = ['rbrl002', 'backlog', '2022', .000000211, 4, 2, 3, 4, 5]
        self.assertEqual(accession_list, accession_list_expected, "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
