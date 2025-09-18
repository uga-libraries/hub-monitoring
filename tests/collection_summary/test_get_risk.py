"""
Tests for the function get_risk(), which gets the number of files at each risk level.
"""
import unittest
from collection_summary import get_risk
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_all_risks_once(self):
        """Test for when there is one file for each risk level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-01-er')
        risk = get_risk(acc_path)
        expected = [1, 1, 1, 1, None]
        self.assertEqual(expected, risk, "Problem with test for all risks once")

    def test_all_risks_repeated(self):
        """Test for when there are a different number of files for each risk level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-02-er')
        risk = get_risk(acc_path)
        expected = [5, 4, 3, 2, None]
        self.assertEqual(expected, risk, "Problem with test for all risks repeated")

    def test_duplicates(self):
        """Test for when all files are in the risk CSV more than once, with the same risk level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2021-11-er')
        risk = get_risk(acc_path)
        expected = [1, 0, 1, 2, None]
        self.assertEqual(expected, risk, "Problem with test for duplicates, all files")

    def test_duplicates_mix(self):
        """Test for when files are in the risk CSV 3 times, twice with the same risk level and once with a different"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2021-12-er')
        risk = get_risk(acc_path)
        expected = [2, 1, 2, 3, None]
        self.assertEqual(expected, risk, "Problem with test for duplicates, some files")

    def test_duplicates_partial(self):
        """Test for when some files are in the risk CSV more than once, with the same risk level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2021-13-er')
        risk = get_risk(acc_path)
        expected = [1, 1, 0, 2, None]
        self.assertEqual(expected, risk, "Problem with test for duplicates, some files")

    def test_no_risk_csv(self):
        """Test for the returned value when the accession has no risk csv"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2021-40-er')
        risk = get_risk(acc_path)
        expected = [0, 0, 0, 0, 'Accession 2021-40-er has no risk csv. ']
        self.assertEqual(expected, risk, "Problem with test for no risk csv")

    def test_one_risk(self):
        """Test for when there is one file with one risk level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-03-er')
        risk = get_risk(acc_path)
        expected = [0, 0, 0, 1, None]
        self.assertEqual(expected, risk, "Problem with test for one risk once")

    def test_one_risk_repeated(self):
        """Test for when there is one file with multiple risk levels"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-04-er')
        risk = get_risk(acc_path)
        expected = [0, 0, 1, 1, None]
        self.assertEqual(expected, risk, "Problem with test for one risk repeated")

    def test_two_risks(self):
        """Test for when there are multiple files for two risk levels and no files for the other two risk levels"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-05-er')
        risk = get_risk(acc_path)
        expected = [0, 2, 3, 0, None]
        self.assertEqual(expected, risk, "Problem with test for two risks repeated")

    def updated_column_name(self):
        """Test for when the NARA column has the updated name, NARA_Risk_Level instead of NARA_Risk Level"""
        acc_path = join('test_data', 'Russell_Hub', 'backlogged', 'rbrl002', '2022-06-er')
        risk = get_risk(acc_path)
        expected = [0, 2, 3, 0, None]
        self.assertEqual(expected, risk, "Problem with test for updated column name")


if __name__ == '__main__':
    unittest.main()
