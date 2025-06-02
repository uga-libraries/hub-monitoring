"""
Test for the function fixity_validation_log(), which makes a log with all accessions to be validated.
"""
from datetime import date
import os
import unittest
from validate_fixity import fixity_validation_log
from test_script_validate_fixity import csv_to_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the test output if it was created"""
        folders = ['acc_bag', 'acc_zip', 'extra_status', 'no_acc', 'no_fixity']
        log_name = f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"
        for folder in folders:
            log_path = os.path.join(os.getcwd(), 'test_data', 'log', folder, 'born-digital', log_name)
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_acc_bag(self):
        """Test for when the accessions are in bags for fixity validation"""
        # Makes the variable for function input and runs the function.
        acc_dir = os.path.join('test_data', 'log', 'acc_bag', 'born-digital')
        fixity_validation_log(acc_dir)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity', 'Result'],
                    ['backlogged', 'harg_ms1234 papers', '2021_12_er',
                     os.path.join(acc_dir, 'backlogged', 'harg_ms1234 papers', '2021_12_er'),
                     'Bag', '2021_12_er_bag', 'BLANK'],
                    ['backlogged', 'harg_ms1234 papers', '2021_345_ER',
                     os.path.join(acc_dir, 'backlogged', 'harg_ms1234 papers', '2021_345_ER'),
                     'Bag', '2021_345_ER_bag', 'BLANK'],
                    ['closed', 'harg_ms1000 papers', '2001_01_er',
                     os.path.join(acc_dir, 'closed', 'harg_ms1000 papers', '2001_01_er'),
                     'Bag', '2001_01_er_bag', 'BLANK'],
                    ['closed', 'harg_ms2000 papers', '2002_02_er',
                     os.path.join(acc_dir, 'closed', 'harg_ms2000 papers', '2002_02_er'),
                     'Bag', '2002_02_er_bag', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for acc_bag")

    def test_acc_zip(self):
        """Test for when the accessions are zipped with a md5 in a text file for fixity validation"""
        # Makes the variable for function input and runs the function.
        acc_dir = os.path.join('test_data', 'log', 'acc_zip', 'born-digital')
        fixity_validation_log(acc_dir)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity', 'Result'],
                    ['backlogged', 'rbrl123', '2010-01-er',
                     os.path.join(acc_dir, 'backlogged', 'rbrl123', '2010-01-er'),
                     'Zip', '2010-01-er_zip_md5.txt', 'BLANK'],
                    ['backlogged', 'rbrl123', '2010-02-er',
                     os.path.join(acc_dir, 'backlogged', 'rbrl123', '2010-02-er'),
                     'Zip', '2010-02-er_zip_md5.txt', 'BLANK'],
                    ['backlogged', 'rbrl456abc', '2010-06-er',
                     os.path.join(acc_dir, 'backlogged', 'rbrl456abc', '2010-06-er'),
                     'Zip', '2010-06-er_zip_md5.txt', 'BLANK'],
                    ['closed', 'rbrl333', 'no-acc-num',
                     os.path.join(acc_dir, 'closed', 'rbrl333', 'no-acc-num'),
                     'Zip', 'no-acc-num_zip_md5.txt', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for acc_zip")

    def test_extra_status(self):
        """Test for when there is another folder at the "status" level (not included in log)"""
        # Makes the variable for function input and runs the function.
        acc_dir = os.path.join('test_data', 'log', 'extra_status', 'born-digital')
        fixity_validation_log(acc_dir)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity', 'Result'],
                    ['closed', 'rbrl333', 'no-acc-num', os.path.join(acc_dir, 'closed', 'rbrl333', 'no-acc-num'),
                     'Bag', 'no-acc-num_bag', 'BLANK']]
        self.assertEqual(result, expected, "Problem with test for extra_status")

    def test_no_acc(self):
        """Test for when there are folders at the "accession" level that aren't accessions (included in log)"""
        # Makes the variable for function input and runs the function.
        acc_dir = os.path.join('test_data', 'log', 'no_acc', 'Born-digital')
        fixity_validation_log(acc_dir)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity', 'Result'],
                    ['backlogged', 'ua22-333 records', '2022-1-er',
                     os.path.join(acc_dir, 'backlogged', 'ua22-333 records', '2022-1-er'),
                     'Bag', '2022-1-er_bag', 'BLANK'],
                    ['backlogged', 'ua22-333 records', 'Appraisal copy',
                     os.path.join(acc_dir, 'backlogged', 'ua22-333 records', 'Appraisal copy'),
                     'BLANK', 'BLANK', 'Not an accession'],
                    ['closed', 'harg1234', 'access', os.path.join(acc_dir, 'closed', 'harg1234', 'access'),
                     'BLANK', 'BLANK', 'Not an accession']]
        self.assertEqual(result, expected, "Problem with test for no_acc")

    def test_no_fixity(self):
        """Test for when there are folders that are accessions but don't have fixity information  (included in log)"""
        # Makes the variable for function input and runs the function.
        acc_dir = os.path.join('test_data', 'log', 'no_fixity', 'born-digital')
        fixity_validation_log(acc_dir)

        # Verifies the log has the correct values.
        result = csv_to_list(os.path.join(acc_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Fixity', 'Result'],
                    ['closed', 'rbrl333', '2002_02_er', os.path.join(acc_dir, 'closed', 'rbrl333', '2002_02_er'),
                     'BLANK', 'BLANK', 'No fixity information'],
                    ['closed', 'rbrl333', 'no-acc-num', os.path.join(acc_dir, 'closed', 'rbrl333', 'no-acc-num'),
                     'BLANK', 'BLANK', 'No fixity information']]
        self.assertEqual(result, expected, "Problem with test for no_acc")


if __name__ == '__main__':
    unittest.main()
