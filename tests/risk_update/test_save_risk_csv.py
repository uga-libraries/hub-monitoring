"""
Tests for the function save_risk_csv(), which save the updated risk information to a CSV.

To simplify the test, the new_risk_df is made within the test and only has a few of the total columns.
"""
import unittest
from risk_update import save_risk_csv
from test_script_risk_update import csv_to_list
from datetime import datetime
from os.path import join
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def test_duplicates(self):
        """Test for when the risk information includes duplicate rows"""
         # Creates input variables and runs the function.
        root = join('test_data', 'Russell_Hub', 'rbrl004', '2005-10-er')
        new_risk_df = DataFrame()
        save_risk_csv(root, new_risk_df)

        # Tests the contents of the csv are correct.
        result = csv_to_list(join(root, f"2005-10-er_full_risk_data{datetime.today().strftime('%Y-%m-%d')}.csv"))
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
