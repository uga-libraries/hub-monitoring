"""
Test for the function get_date(), which gets the year the accession was copied.
"""
import unittest
from collection_summary import get_date
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        """Test for when the accession number starts with the year"""
        dept_hub = join(getcwd(), '..', 'test_data', 'Collection_Summary', 'Hargrett_Hub')
        acc_path = join(dept_hub, 'backlog', 'ua01-001 Dept records', 'ua01-001_032')
        date = get_date(acc_path)
        self.assertEqual(date, '2024', "Problem with test for the function")


if __name__ == '__main__':
    unittest.main()
