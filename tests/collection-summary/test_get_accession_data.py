"""
Test for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import os
import unittest
from collection_summary import get_accession_data


class MyTestCase(unittest.TestCase):

    def test_function(self):
        path = os.path.join(os.getcwd(), '..', 'test_data', 'backlog', 'coll-002', '2022-01')
        accession_list = get_accession_data(path)
        accession_list_expected = [.000000211, 4, '2024-02-09', 2, 3, 4, 5]
        self.assertEqual(accession_list, accession_list_expected, "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
