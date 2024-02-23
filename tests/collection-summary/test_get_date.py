"""
Tests for the function get_date(), which gets the year of the accession.
"""
import unittest
from collection_summary import get_date
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_accession_number(self):
        """Test for when the accession number starts with the year"""
        path = join(getcwd(), '..', 'test_data', 'Hargrett_Hub', 'backlog', 'ua01-001 Dept records', '2009_ua01-001')
        date = get_date(path)
        self.assertEqual(date, '2009', "Problem with test for accession number")

    def test_log(self):
        """Test for when the accession number does not start with the year, so it uses the preservation log file"""
        path = join(getcwd(), '..', 'test_data', 'Hargrett_Hub', 'backlog', 'ua01-001 Dept records', 'ua01-001_033')
        date = get_date(path)
        self.assertEqual(date, '2024', "Problem with test for log")


if __name__ == '__main__':
    unittest.main()
