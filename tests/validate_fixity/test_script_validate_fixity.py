"""
Tests for the script validate_fixity.py, which validates accession fixity, updates the logs, and makes a report.
"""
import subprocess
import unittest
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

    def test_correct(self):
        """Test for when the script runs correctly on all accessions in Validate_Fixity_Hub, collection test_003"""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), '..', 'test_data', 'Validate_Fixity_Hub', 'test_003_log_update')
        subprocess.run(f'python {script} {directory}', shell=True)

        # Verifies the contents of the log for 2023_test003_001_er have been updated.
        df = read_csv(join(directory, '2023_test003_001_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.001',
                     'Bagged with accession 2023.test003.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Copied to external storage device using TeraCopy. No security threats were detected.',
                     'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'CD.002',
                     'Bagged with accession 2023.test003.001.ER. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', '2023-02-28', 'nan',
                     'Validated bag for accession 2023.test003.001.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.001.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test003.001.ER. The bag was not valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_001_er')

        # Verifies the contents of the log for 2023_test003_002_er have been updated.
        df = read_csv(join(directory, '2023_test003_002_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.001',
                     'Bagged with accession 2023.test003.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Copied to external storage device using TeraCopy. No security threats were detected.',
                     'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'CD.002',
                     'Bagged with accession 2023.test003.002.ER. No security threats were detected.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', '2023-02-28', 'nan',
                     'Validated bag for accession 2023.test003.002.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.003', '2023.test003.002.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test003.002.ER. The bag was valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_002_er')

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join('test_data', 'Error_Hub')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python {script} {directory}', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python {script} {directory}', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error_Hub' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")


if __name__ == '__main__':
    unittest.main()
