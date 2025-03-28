"""
Tests for the script validate_fixity.py, which validates accession fixity, updates the logs, and makes a report.
"""
import csv
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

        # For each accession, replaces the updated log with a copy of the original log from the accession folder.
        accessions = [join('test_data', 'test_script_mix', 'backlogged', 'test_001', '2023_test001_002_er'),
                      join('test_data', 'test_script_mix', 'backlogged', 'test_001', '2023_test001_004_er'),
                      join('test_data', 'test_script_mix', 'backlogged', 'test_005', '2023_test005_001_er'),
                      join('test_data', 'test_script_restart', 'backlogged', 'coll_2023', '2023_test004_002_er'),
                      join('test_data', 'test_script_restart', 'backlogged', 'coll_2023', '2023_test005_004_er'),
                      join('test_data', 'test_script_valid', 'closed', 'test_001', '2023_test001_001_er'),
                      join('test_data', 'test_script_valid', 'closed', 'test_004', '2023_test004_003_er')]
        for accession in accessions:
            copyfile(join(accession, 'preservation_log_copy.txt'), join(accession, 'preservation_log.txt'))

        # Deletes any test output that is present.
        today = date.today().strftime('%Y-%m-%d')
        outputs = [join('test_data', 'test_script_mix', f'fixity_validation_log_{today}.csv'),
                   join('test_data', 'test_script_mix', '2023_test005_001_er_manifest_validation_errors.csv'),
                   join('test_data', 'test_script_restart', '2023_test005_004_er_manifest_validation_errors.csv'),
                   join('test_data', 'test_script_restart', f"fixity_validation_log_{today}.csv"),
                   join('test_data', 'test_script_valid', f'fixity_validation_log_{today}.csv')]
        for output in outputs:
            if exists(output):
                remove(output)

    def test_mix(self):
        """Test for when the script runs correctly on a mix of valid and not valid accessions,
        as well as an accession without a preservation log."""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = join(getcwd(), 'test_data', 'test_script_mix')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about the missing preservation log and validation errors.
        result = output.stdout.decode('utf-8')
        expected = (f'Starting on accession {input_directory}\\backlogged\\test_001\\2023_test001_002_er (Bag)\r\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_001\\2023_test001_004_er (Bag)\r\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_005\\2023_test005_001_er (InitialManifest)\r\n'
                    f'Starting on accession {input_directory}\\closed\\test_123\\2023_test123_001_er (InitialManifest)\r\n'
                    'ERROR: accession 2023_test123_001_er has no preservation log.\r\n\r\n'
                    '\r\nValidation errors found, see fixity_validation_log.csv in the input_directory.\r\n')
        self.assertEqual(result, expected, 'Problem with test for mix, printed message')

        # Verifies the contents of the fixity validation log are correct.
        result = csv_to_list(join(input_directory, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Bag_Name', 'Manifest_Name',
                     'Validation_Result'],
                    ['backlogged', 'test_001', '2023_test001_002_er',
                     join(input_directory, 'backlogged', 'test_001', '2023_test001_002_er'), 'Bag',
                     '2023_test001_002_er_bag', 'nan', 'Valid'],
                    ['backlogged', 'test_001', '2023_test001_004_er',
                     join(input_directory, 'backlogged', 'test_001', '2023_test001_004_er'), 'Bag',
                     '2023_test001_004_er_bag', 'nan',
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'],
                    ['backlogged', 'test_005', '2023_test005_001_er',
                     join(input_directory, 'backlogged', 'test_005', '2023_test005_001_er'), 'InitialManifest',
                     'nan', 'initialmanifest_20230501.csv', '2 manifest errors'],
                    ['closed', 'test_123', '2023_test123_001_er',
                     join(input_directory, 'closed', 'test_123', '2023_test123_001_er'), 'InitialManifest',
                     'nan', 'initialmanifest_20230501.csv', 'Valid']]
        self.assertEqual(result, expected, 'Problem with test for mix, validation report')

        # Verifies the contents of the preservation log for 2023_test001_002_er have been updated.
        result = csv_to_list(join(input_directory, 'backlogged', 'test_001', '2023_test001_002_er',
                                  'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for mix, 2023_test001_002_er preservation log')

        # Verifies the contents of the preservation log for 2023_test001_004_er have been updated.
        result = csv_to_list(join(input_directory, 'backlogged', 'test_001', '2023_test001_004_er',
                                  'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.4.ER. The bag is not valid. Bag validation failed: '
                     'data\\CD_2\\File2.txt md5 validation failed: expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" '
                     'found="85c8fbcb2ff1d73cb94ed9c355eb20d5"', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for mix, 2023_test001_004_er preservation log')

        # Verifies the contents of the preservation log for 2023_test005_001_er have been updated.
        result = csv_to_list(join(input_directory, 'backlogged', 'test_005', '2023_test005_001_er',
                                  'preservation_log.txt'), delimiter='\t')
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
        result = csv_to_list(join(input_directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_001_er\\CD_1\\File1.txt', 'CA1EA02C10B7C37F425B9B7DD86D5E11', 'Manifest'],
                    ['Number of files does not match. 1 files in the accession folder and 2 in the manifest.',
                     'nan', 'nan']]
        self.assertEqual(result, expected, 'Problem with for mix, 2023_test005_001_er manifest log')

    def test_restart(self):
        """Test for when the script is being restarted after a break
        and uses a pre-existing fixity validation log where some accessions already have a validation result"""
        input_directory = join(getcwd(), 'test_data', 'test_script_restart')

        # Makes the fixity validation log.
        coll_path = join(input_directory, 'backlogged', 'coll_2023')
        rows = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Bag_Name', 'Manifest_Name',
                 'Validation_Result'],
                ['backlogged', 'coll_2023', '2023_test001_001_er', join(coll_path, '2023_test001_001_er'),
                 'Bag', '2023_test001_001_er_bag', None, 'Valid'],
                ['backlogged', 'coll_2023', '2023_test001_005_er', join(coll_path, '2023_test001_005_er'),
                 'Bag', '2023_test001_005_er_bag', None, 'Bag validation failed'],
                ['backlogged', 'coll_2023', '2023_test004_002_er', join(coll_path, '2023_test004_002_er'),
                 'InitialManifest', None, 'initialmanifest_20231124.csv', None],
                ['backlogged', 'coll_2023', '2023_test005_004_er', join(coll_path, '2023_test005_004_er'),
                 'InitialManifest', None, 'initialmanifest_20230521.csv', None]]
        log_path = join(input_directory, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
        with open(log_path, 'w', newline='') as open_log:
            log_writer = csv.writer(open_log)
            log_writer.writerows(rows)

        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about validation errors.
        result = output.stdout.decode('utf-8')
        expected = (f'Starting on accession {coll_path}\\2023_test004_002_er (InitialManifest)\r\n'
                    f'Starting on accession {coll_path}\\2023_test005_004_er (InitialManifest)\r\n'
                    '\r\nValidation errors found, see fixity_validation_log.csv in the input_directory.\r\n')
        self.assertEqual(result, expected, 'Problem with test for restart, printed message')

        # Verifies the contents of the fixity validation log are correct.
        result = csv_to_list(join(input_directory, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Bag_Name',
                     'Manifest_Name', 'Validation_Result'],
                    ['backlogged', 'coll_2023', '2023_test001_001_er', join(coll_path, '2023_test001_001_er'),
                     'Bag', '2023_test001_001_er_bag', 'nan', 'Valid'],
                    ['backlogged', 'coll_2023', '2023_test001_005_er', join(coll_path, '2023_test001_005_er'),
                     'Bag', '2023_test001_005_er_bag', 'nan', 'Bag validation failed'],
                    ['backlogged', 'coll_2023', '2023_test004_002_er', join(coll_path, '2023_test004_002_er'),
                     'InitialManifest', 'nan', 'initialmanifest_20231124.csv', 'Valid'],
                    ['backlogged', 'coll_2023', '2023_test005_004_er', join(coll_path, '2023_test005_004_er'),
                     'InitialManifest', 'nan', 'initialmanifest_20230521.csv', '1 manifest errors']]
        self.assertEqual(result, expected, 'Problem with test for restart, fixity validation log')

        # Verifies the contents of the preservation log for 2023_test004_002_er have been updated.
        result = csv_to_list(join(input_directory, 'backlogged', 'coll_2023', '2023_test004_002_er',
                                  'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'nan', "Can't bag; made manifest.", 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T4', '2023.T4.02.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T4.02.ER. The manifest is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for restart, 2023_test004_002_er preservation log')

        # Verifies the contents of the preservation log for 2023_test005_004_er have been updated.
        result = csv_to_list(join(input_directory, 'backlogged', 'coll_2023', '2023_test005_004_er',
                                  'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'nan', "Can't bag; made manifest.", 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'nan', 'Validated manifest. Valid.', 'JD'],
                    ['T5', '2023.T5.04.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.T5.04.ER. The manifest is not valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for restart, 2023_test005_004_er preservation log')

        # Verifies the contents of the  manifest log for 2023_test005_004_er are correct.
        result = csv_to_list(join(input_directory, '2023_test005_004_er_manifest_validation_errors.csv'))
        expected = [['File', 'MD5', 'MD5_Source'],
                    [join(coll_path, '2023_test005_004_er', '2023_test005_004_er', 'CD_2', 'File1.txt'),
                     '717216B472AA04EB2E615809C7F30C4E', 'Current']]
        self.assertEqual(result, expected, 'Problem with for restart, 2023_test005_004_er manifest log')

    def test_valid(self):
        """Test for when the script runs correctly and both accessions are valid
        There are also a folder and file that the script should skip
        and accession 2023_test001_001_er contains a manifest that the script should skip as well as being in a bag.
        """
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = join(getcwd(), 'test_data', 'test_script_valid')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about validation errors.
        result = output.stdout.decode('utf-8')
        status_path = join(getcwd(), 'test_data', 'test_script_valid', 'closed')
        expected = (f'Starting on accession {status_path}\\test_001\\2023_test001_001_er (Bag)\r\n'
                    f'Starting on accession {status_path}\\test_004\\2023_test004_003_er (InitialManifest)\r\n'
                    '\r\nNo validation errors.\r\n')
        self.assertEqual(result, expected, 'Problem with test for valid, printed message')

        # Verifies the contents of the fixity validation log.
        result = csv_to_list(join(input_directory, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Accession_Path', 'Fixity_Type', 'Bag_Name', 'Manifest_Name',
                     'Validation_Result'],
                    ['closed', 'test_001', '2023_test001_001_er',
                     join(getcwd(), 'test_data', 'test_script_valid', 'closed', 'test_001', '2023_test001_001_er'),
                     'Bag', '2023_test001_001_er_bag', 'nan', 'Valid'],
                    ['closed', 'test_004', '2023_test004_003_er',
                     join(getcwd(), 'test_data', 'test_script_valid', 'closed', 'test_004', '2023_test004_003_er'),
                     'InitialManifest', 'nan', 'initialmanifest_20240426.csv', 'Valid']]
        self.assertEqual(result, expected, 'Problem with test for valid, fixity validation log')

        # Verifies the contents of the preservation log for 2023_test001_001_er have been updated.
        result = csv_to_list(join(input_directory, 'closed', 'test_001', '2023_test001_001_er',
                                  'preservation_log.txt'), delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-31', 'nan', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.1.1.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(result, expected, 'Problem with test for valid, 2023_test001_001_er preservation log')

        # Verifies the contents of the preservation log for 2023_test004_003_er have been updated.
        result = csv_to_list(join(input_directory, 'closed', 'test_004', '2023_test004_003_er',
                                  'preservation_log.txt'), delimiter='\t')
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
        input_directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{input_directory}"', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided input_directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, 'Problem with test for script argument error, printed error')


if __name__ == '__main__':
    unittest.main()
