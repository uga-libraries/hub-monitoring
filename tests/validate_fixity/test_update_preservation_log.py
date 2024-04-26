"""
Tests for the function update_preservation_log(), which adds validation information to an accession's preservation log.
"""
import unittest
from validate_fixity import update_preservation_log
from datetime import date
from os import getcwd
from os.path import join
from pandas import read_csv
from shutil import copyfile


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder"""
        # Accession 2023_test003_001_er
        test1 = join(getcwd(), '..', 'test_data', 'Validate_Fixity', 'test_003_log_update', '2023_test003_001_er')
        copyfile(join(test1, 'preservation_log_copy.txt'), join(test1, 'preservation_log.txt'))

        # Accession 2023_test003_002_er
        test2 = join(getcwd(), '..', 'test_data', 'Validate_Fixity', 'test_003_log_update', '2023_test003_002_er')
        copyfile(join(test2, 'preservation_log_copy.txt'), join(test2, 'preservation_log.txt'))

    def test_bag_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        root = join(getcwd(), '..', 'test_data', 'Validate_Fixity', 'test_003_log_update', '2023_test003_001_er')
        update_preservation_log(root, False, 'bag')

        # Verifies the contents of the log have been updated.
        df = read_csv(join(root, 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD1', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'CD2', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', '2023-02-28', 'nan', 'Validated bag for accession. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.1.ER. The bag is not valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for not valid bag')

    def test_bag_valid(self):
        """Test for when the bag is valid"""
        # Makes the variables needed for function input and runs the function.
        root = join(getcwd(), '..', 'test_data', 'Validate_Fixity', 'test_003_log_update', '2023_test003_002_er')
        update_preservation_log(root, True, 'bag')

        # Verifies the contents of the log have been updated.
        df = read_csv(join(root, 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD1', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'CD2', 'Bagged with accession.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', '2023-02-28', 'nan', 'Validated bag for accession. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.3.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for valid bag')


if __name__ == '__main__':
    unittest.main()
