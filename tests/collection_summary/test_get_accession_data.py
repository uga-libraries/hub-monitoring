"""
Test for the function get_accession_data(), which gets the size, date, and risk profile of an accession.
"""
import unittest
from collection_summary import get_accession_data
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        dept_hub = join(getcwd(), '..', 'test_data', 'Collection_Summary', 'Hargrett_Hub')
        accession_list = get_accession_data(dept_hub, 'backlogged', 'ms0001 Person papers', 'ms2022-15-er')
        accession_list_expected = ['ms0001 Person papers', 'backlogged', '2024', .00001, 3, 0, 0, 1, 2]
        self.assertEqual(accession_list, accession_list_expected, "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
