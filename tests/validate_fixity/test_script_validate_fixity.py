"""
Tests for the script validate_fixity.py, which validates accession fixity, updates the logs, and makes a report.
"""
import subprocess
import unittest
from datetime import date
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv
from shutil import copyfile


def csv_to_list(csv_path, delimiter=','):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Delimiter is supplied so this works on the preservation log, which is tab separated instead of commas.
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = read_csv(csv_path, delimiter=delimiter)
    df = df.fillna('nan')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder,
        and delete all other test outputs if they were created."""
        # List of paths for accession with logs to replace.
        accessions = [join('test_data', 'test_script_mix', '2023_test001_002_er'),
                      join('test_data', 'test_script_mix', '2023_test002_004_er'),
                      join('test_data', 'test_script_mix', '2023_test005_001_er'),
                      join('test_data', 'test_script_valid', '2023_test001_001_er'),
                      join('test_data', 'test_script_valid', '2023_test004_003_er')]

        # For each accession, replaces the updated log with a copy of the original log from the accession folder.
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # List of paths for possible test outputs that should be deleted.
        today = date.today().strftime('%Y-%m-%d')
        outputs = [join('test_data', 'test_script_mix', f'fixity_validation_{today}.csv'),
                   join('test_data', 'test_script_mix', '2023_test005_001_er_manifest_validation_errors.csv')]

        # Deletes any test output that is present.
        for output in outputs:
            if exists(output):
                remove(output)

    def test_mix(self):
        """Test for when the script runs correctly on a mix of valid and not valid accessions,
        as well as an accession without a preservation log."""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), 'test_data', 'test_script_mix')
        output = subprocess.run(f'python "{script}" "{directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about the missing preservation log and validation errors.
        result = output.stdout.decode('utf-8')
        expected = (f'Starting on accession {directory}\\2023_test001_002_er (bag)\r\n'
                    f'Starting on accession {directory}\\2023_test002_004_er (bag)\r\n'
                    f'Starting on accession {directory}\\2023_test005_001_er (manifest)\r\n'
                    f'Starting on accession {directory}\\2023_test123_001_er (manifest)\r\n'
                    'ERROR: accession 2023_test123_001_er has no preservation log.\r\n\r\n'
                    '\r\nValidation errors found, see fixity_validation.csv in the directory '
                    'provided as the script argument.\r\n')
        self.assertEqual(result, expected, 'Problem with test for mix, printed message')

        # Verifies the contents of the validation report are correct.
        result = csv_to_list(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Validation_Error'],
                    ['test_data', 'test_script_mix', '2023_test002_004_er',
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'],
                    ['test_data', 'test_script_mix', '2023_test005_001_er', '2 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for mix, validation report')

        # Verifies the contents of the preservation log for 2023_test001_002_er have been updated.
        result = csv_to_list(join(directory, '2023_test001_002_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for mix, 2023_test001_002_er preservation log')

        # Verifies the contents of the preservation log for 2023_test002_004_er have been updated.
        result = csv_to_list(join(directory, '2023_test002_004_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.2', '2023.2.4.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.2.4.ER. The bag is not valid. Bag validation failed: '
                     'data\\CD_2\\File2.txt md5 validation failed: expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" '
                     'found="85c8fbcb2ff1d73cb94ed9c355eb20d5"', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for mix, 2023_test002_004_er preservation log')

        # Verifies the contents of the preservation log for 2023_test005_001_er have been updated.
        result = csv_to_list(join(directory, '2023_test005_001_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'CD.001', 'Copied.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'CD.002', 'Copied.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'nan', 'Can\'t bag; made manifest.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.test005.001.ER. The manifest is not valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for mix, 2023_test005_001_er preservation log')

        # Verifies the contents of the  manifest log for 2023_test005_001_er are correct.
        result = csv_to_list(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 2 in the manifest.',
                     'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with for mix, 2023_test005_001_er manifest log')

    def test_valid(self):
        """Test for when the script runs correctly and both accessions are valid
        There are also a folder and file that the script should skip
        and accession 2023_test001_001_er contains a manifest that the script should skip as well as being in a bag.
        """
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), 'test_data', 'test_script_valid')
        output = subprocess.run(f'python "{script}" "{directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about validation errors.
        result = output.stdout.decode('utf-8')
        coll_path = join(getcwd(), 'test_data', 'test_script_valid')
        expected = (f'Starting on accession {coll_path}\\2023_test001_001_er (bag)\r\n'
                    f'Starting on accession {coll_path}\\2023_test004_003_er (manifest)\r\n'
                    '\r\nNo validation errors.\r\n')
        self.assertEqual(result, expected, 'Problem with test for valid, printed message')

        # Verifies the validation report was not made. It is only made for errors.
        report_path = join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
        report_made = exists(report_path)
        self.assertEqual(report_made, False, 'Problem with test for valid, validation report')

        # Verifies the contents of the preservation log for 2023_test001_001_er have been updated.
        result = csv_to_list(join(directory, '2023_test001_001_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.1.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, 2023_test001_001_er preservation log')

        # Verifies the contents of the preservation log for 2023_test004_003_er have been updated.
        result = csv_to_list(join(directory, '2023_test004_003_er', 'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'CD.001', 'Copied.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'CD.002', 'Copied.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'nan', 'Can\'t bag; made manifest.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'nan', 'Validated manifest. Valid.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.test004.003.ER. The manifest is valid.',
                     'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, 2023_test004_003_er preservation log')

    def test_arg_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{directory}"', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python "{script}" "{directory}"', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided input_directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, 'Problem with test for script argument error, printed error')


if __name__ == '__main__':
    unittest.main()
