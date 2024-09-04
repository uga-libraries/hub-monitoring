"""
Tests for the function update_report(), which saves completeness results for an accession to a csv.
"""
import unittest
from accession_completeness_report import update_report
from test_script_accession_completeness_report import csv_to_list
from datetime import date
from os import remove
from os.path import exists, join


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the test output if it was created"""
        today = date.today().strftime('%Y-%m-%d')
        if exists(join('update_report_test_data', f'accession_completeness_report_{today}.csv')):
            remove(join('update_report_test_data', f'accession_completeness_report_{today}.csv'))

    def test_new_report(self):
        """Test for when there is not yet an accession completeness report"""
        # Creates input variables and runs the function.
        accession_path = join('update_report_test_data', 'backlogged', 'coll_1', 'acc_1')
        completeness_dict = {'pres_log': True, 'full_risk': True, 'initial_manifest': True, 'bag': True}
        update_report('update_report_test_data', 'backlogged', 'coll_1', accession_path, completeness_dict)

        # Tests the contents of the csv are correct.
        today = date.today().strftime('%Y-%m-%d')
        result = csv_to_list(join('update_report_test_data', f'accession_completeness_report_{today}.csv'))
        expected = [['Status', 'Collection', 'Accession', 'Preservation_Log', 'Full_Risk', 'Initial_Manifest', 'Bag'],
                    ['backlogged', 'coll_1', 'acc_1', True, True, True, True]]
        self.assertEqual(result, expected, "Problem with test for new report")

    def test_existing_report(self):
        """Test for adding to an existing accession completeness report"""
        # Creates input variables for the first accession and runs the function, which makes the report.
        accession_path = join('update_report_test_data', 'backlogged', 'coll_1', 'acc_1')
        completeness_dict = {'pres_log': True, 'full_risk': True, 'initial_manifest': True, 'bag': True}
        update_report('update_report_test_data', 'backlogged', 'coll_1', accession_path, completeness_dict)

        # Creates input variables for the second accession and runs the function again, which adds to the report.
        accession_path = join('update_report_test_data', 'backlogged', 'coll_1', 'acc_2')
        completeness_dict = {'pres_log': False, 'full_risk': False, 'initial_manifest': True, 'bag': True}
        update_report('update_report_test_data', 'backlogged', 'coll_1', accession_path, completeness_dict)

        # Tests the contents of the csv are correct.
        today = date.today().strftime('%Y-%m-%d')
        result = csv_to_list(join('update_report_test_data', f'accession_completeness_report_{today}.csv'))
        expected = [['Status', 'Collection', 'Accession', 'Preservation_Log', 'Full_Risk', 'Initial_Manifest', 'Bag'],
                    ['backlogged', 'coll_1', 'acc_1', True, True, True, True],
                    ['backlogged', 'coll_1', 'acc_2', False, False, True, True]]
        self.assertEqual(result, expected, "Problem with test for existing report")


if __name__ == '__main__':
    unittest.main()
