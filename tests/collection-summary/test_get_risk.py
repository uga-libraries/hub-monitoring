"""
Tests for the function get_risk(), which gets the number of files at each risk level.
"""
import unittest
from collection_summary import get_risk
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_all_risks_once(self):
        """Test for when there is one file of each risk in the accession."""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-001', '2021-01')
        risk = get_risk(path)
        risk_expected = [1, 1, 1, 1]
        self.assertEqual(risk, risk_expected, "Problem with test for all risks once")

    def test_all_risks_repeated(self):
        """Test for when there are all risk levels: 2 no match, 3 high, 4 moderate, and 5 low."""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-002', '2022-01')
        risk = get_risk(path)
        risk_expected = [2, 3, 4, 5]
        self.assertEqual(risk, risk_expected, "Problem with test for all risks repeated")

    def test_one_risk(self):
        """Test for when there is a single file (low risk) in the accession."""
        path = join(getcwd(), '..', 'test_data', 'backlog', 'coll-002', '2022-02')
        risk = get_risk(path)
        risk_expected = [0, 0, 0, 1]
        self.assertEqual(risk, risk_expected, "Problem with test for one risk")

    def test_two_risks(self):
        """Test for when there is one file of moderate risk and three of low risk."""
        path = join(getcwd(), '..', 'test_data', 'closed', 'coll-003', '2023-01')
        risk = get_risk(path)
        risk_expected = [0, 0, 1, 3]
        self.assertEqual(risk, risk_expected, "Problem with test for two risks")


if __name__ == '__main__':
    unittest.main()
