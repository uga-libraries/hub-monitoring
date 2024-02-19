"""
Tests for the function get_risk(), which gets the number of files at each risk level.
"""
import unittest
from collection_summary import get_risk
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_all_risks_once(self):
        """Test for when there is one file for each risk level"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-01-er')
        risk = get_risk(path)
        risk_expected = [1, 1, 1, 1]
        self.assertEqual(risk, risk_expected, "Problem with test for all risks once")

    def test_all_risks_repeated(self):
        """Test for when there are a different number of files for each risk level"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-02-er')
        risk = get_risk(path)
        risk_expected = [5, 4, 3, 2]
        self.assertEqual(risk, risk_expected, "Problem with test for all risks repeated")

    def test_one_risk(self):
        """Test for when there is one file with one risk level"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-03-er')
        risk = get_risk(path)
        risk_expected = [0, 0, 0, 1]
        self.assertEqual(risk, risk_expected, "Problem with test for one risk once")

    def test_one_risk_repeated(self):
        """Test for when there is one file with multiple risk levels"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-04-er')
        risk = get_risk(path)
        risk_expected = [0, 0, 1, 1]
        self.assertEqual(risk, risk_expected, "Problem with test for one risk repeated")

    def test_two_risks(self):
        """Test for when there are multiple files for two risk levels and no files for the other two risk levels"""
        path = join(getcwd(), '..', 'test_data', 'Russell_Hub', 'backlog', 'rbrl002', '2022-05-er')
        risk = get_risk(path)
        risk_expected = [0, 2, 3, 0]
        self.assertEqual(risk, risk_expected, "Problem with test for two risks repeated")


if __name__ == '__main__':
    unittest.main()
