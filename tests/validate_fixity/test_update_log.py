"""
Tests for the function update_log(), which adds validation information to an accession's preservation log.
"""
import unittest
from validate_fixity import update_log
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
        test1 = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_003_log_update', '2023_test003_001_er')
        copyfile(join(test1, 'preservation_log_copy.txt'), join(test1, 'preservation_log.txt'))

        # Accession 2023_test003_002_er
        test2 = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_003_log_update', '2023_test003_002_er')
        copyfile(join(test2, 'preservation_log_copy.txt'), join(test2, 'preservation_log.txt'))

    def test_not_valid(self):
        """Test for when the bag is not valid"""
        # Makes the variables needed for function input and runs the function.
        parent = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_003_log_update', '2023_test003_001_er')
        bag_path = join(parent, '2023_test003_001_er_bag')
        validation = 'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 28 bytes'
        update_log(bag_path, validation)

        # Verifies the contents of the log have been updated.
        df = read_csv(join(parent, 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Virus scanned using Micorosoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Bagged with accession 2023.test003.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Virus scanned using Micorosoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Copied to external storage device using TeraCopy. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Bagged with accession 2023.test003.001.ER. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'nan',
                     'Validated bag for accession 2023.test003.001.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test003.001.ER. The bag was not valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for not valid bag')

    def test_valid(self):
        """Test for when the bag is valid"""
        # Makes the variables needed for function input and runs the function.
        parent = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_003_log_update', '2023_test003_002_er')
        bag_path = join(parent, '2023_test003_002_er_bag')
        validation = 'Bag valid'
        update_log(bag_path, validation)

        # Verifies the contents of the log have been updated.
        df = read_csv(join(parent, 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Virus scanned using Micorosoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Bagged with accession 2023.test003.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Virus scanned using Micorosoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Copied to external storage device using TeraCopy. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Bagged with accession 2023.test003.002.ER. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'nan',
                     'Validated bag for accession 2023.test003.002.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test003.002.ER. The bag was valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for valid bag')


if __name__ == '__main__':
    unittest.main()
