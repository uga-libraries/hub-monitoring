"""
Test for the function get_date(), which gets the year the accession was copied.
"""
import unittest
from collection_summary import get_date
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for when the accession number starts with the year"""
        acc_path = join('test_data', 'Hargrett_Hub', 'backlogged', 'ua01-001 Dept records', 'ua_01_032_ER')
        date = get_date(acc_path)
        self.assertEqual('2024', date, "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
