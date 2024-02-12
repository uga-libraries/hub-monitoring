"""
Tests for the function get_date(), which gets the date of the accession.
"""
import unittest
from collection_summary import get_date
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_log(self):
        """Test for an accession that does have a preservation log file."""
        path = join(getcwd(), '..', 'test_data', 'closed', 'coll-003', '2023-01')
        date = get_date(path)
        self.assertEqual(date, '2024-02-09', "Problem with test for log")

    def test_no_log(self):
        """Test for an accession that does not have a preservation log file."""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-002', '2022-02')
        date = get_date(path)
        self.assertEqual(date, '2022', "Problem with test for no log")


if __name__ == '__main__':
    unittest.main()
