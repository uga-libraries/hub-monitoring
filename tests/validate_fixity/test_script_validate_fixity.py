"""
Tests for the script validate_fixity.py, which validates accession fixity, updates the logs, and makes a report.

Note: the fixity validation log includes a timestamp to a minute, so if that fails, check if it is just off by minute.
That could mean it is working fine but the clock ticked over 1 minute between making the output and testing it.
"""
import csv
from datetime import date, datetime
import os
import pandas as pd
import shutil
import subprocess
import unittest


def csv_to_list(csv_path, delimiter=','):
    """Read csv into a dataframe, clean up, and return the values of each row as a list
    Delimiter is supplied so this works on the preservation log, which is tab separated instead of commas.
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = pd.read_csv(csv_path, dtype=str, delimiter=delimiter)
    df = df.fillna('BLANK')
    csv_list = [df.columns.tolist()] + df.values.tolist()
    return csv_list


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete the updated preservation log and fixity validation log, if present."""

        # For each accession, deletes the updated preservation from the accession folder.
        accessions = [os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_001', 'AC001_ER'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_001', 'no-acc-num'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_005', 'AC002_ER'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_005', 'no-acc-num'),
                      os.path.join('dup_acc', 'born-digital', 'closed', 'test_123', 'AC001_ER'),
                      os.path.join('mix', 'born-digital', 'backlogged', 'test_001', '2023_test001_002_er'),
                      os.path.join('mix', 'born-digital', 'backlogged', 'test_001', '2023_test001_004_er'),
                      os.path.join('mix', 'born-digital', 'backlogged', 'test_005', '2023_test005_001_er'),
                      os.path.join('restart', 'born-digital', 'backlogged', 'coll_2023', '2023_test004_002_er'),
                      os.path.join('restart', 'born-digital', 'backlogged', 'coll_2023', '2023_test005_004_er'),
                      os.path.join('valid', 'Born-digital', 'closed', 'test_001', '2023_test001_001_er'),
                      os.path.join('valid', 'Born-digital', 'closed', 'test_004', '2023_test004_003_er')]
        for accession in accessions:
            log_path = os.path.join('test_data', 'script', accession, 'preservation_log.txt')
            if os.path.exists(log_path):
                os.remove(log_path)

        # Deletes the fixity validation log, if present.
        input_dirs = [os.path.join('test_data', 'script', 'dup_acc', 'born-digital'),
                      os.path.join('test_data', 'script', 'mix', 'born-digital'),
                      os.path.join('test_data', 'script', 'restart', 'born-digital'),
                      os.path.join('test_data', 'script', 'valid', 'Born-digital')]
        for input_dir in input_dirs:
            log_path = os.path.join(input_dir, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
            if os.path.exists(log_path):
                os.remove(log_path)

    def test_dup_accession(self):
        """Test for when the script runs correctly on accessions with duplicate accession ids"""
        # Makes a copy of the preservation logs, since it will be updated by the test.
        accessions = [os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_001', 'AC001_ER'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_001', 'no-acc-num'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_005', 'AC002_ER'),
                      os.path.join('dup_acc', 'born-digital', 'backlogged', 'test_005', 'no-acc-num'),
                      os.path.join('dup_acc', 'born-digital', 'closed', 'test_123', 'AC001_ER')]
        for accession in accessions:
            shutil.copyfile(os.path.join('test_data', 'script', accession, 'preservation_log_copy.txt'),
                            os.path.join('test_data', 'script', accession, 'preservation_log.txt'))

        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script', 'dup_acc', 'born-digital')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, capture_output=True, text=True)
        today = date.today().strftime('%Y-%m-%d')

        # # Verifies the script printed the correct message about the missing preservation log and validation errors.
        result = output.stdout
        expected = (f'Starting on accession {input_directory}\\backlogged\\test_001\\AC001_ER (Bag)\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_001\\no-acc-num (Bag)\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_005\\AC002_ER (Bag)\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_005\\no-acc-num (Bag)\n'
                    f'Starting on accession {input_directory}\\closed\\test_123\\AC001_ER (Bag)\n'
                    f'Starting on accession {input_directory}\\closed\\test_123\\no-acc-num (Bag)\n'
                    '\nValidation errors found, see the fixity validation log in the input_directory.\n')
        self.assertEqual(expected, result, 'Problem with test for dup_accession, printed message')

        # Verifies the contents of the fixity validation log are correct.
        result = csv_to_list(os.path.join(input_directory, f"fixity_validation_log_{today}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result'],
                    ['backlogged', 'test_001', 'AC001_ER',
                     os.path.join(input_directory, 'backlogged', 'test_001', 'AC001_ER'), 'Bag',
                     'Updated', 'False', datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'Payload-Oxum validation failed. Expected 1 files and 29 bytes but found 2 files and 58 bytes'],
                    ['backlogged', 'test_001', 'no-acc-num',
                     os.path.join(input_directory, 'backlogged', 'test_001', 'no-acc-num'), 'Bag',
                     'Updated', 'False', datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'Payload-Oxum validation failed. Expected 4 files and 43 bytes but found 1 files and 9 bytes'],
                    ['backlogged', 'test_005', 'AC002_ER',
                     os.path.join(input_directory, 'backlogged', 'test_005', 'AC002_ER'), 'Bag',
                     'Updated', 'False', datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'],
                    ['backlogged', 'test_005', 'no-acc-num',
                     os.path.join(input_directory, 'backlogged', 'test_005', 'no-acc-num'), 'Bag',
                     'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'test_123', 'AC001_ER',
                     os.path.join(input_directory, 'closed', 'test_123', 'AC001_ER'), 'Bag',
                     'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'test_123', 'no-acc-num',
                     os.path.join(input_directory, 'closed', 'test_123', 'no-acc-num'), 'Bag',
                     'Log path not found', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, validation report')

        # Verifies the contents of the preservation log for test_001, AC001_ER have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_001', 'AC001_ER', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.001', 'AC001.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.001', 'AC001.ER', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.001', 'AC001.ER', today, 'BLANK',
                     'Validated bag for accession AC001.ER. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 1 files and 29 bytes but found 2 files and 58 bytes',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, test_001/AC001_ER preservation log')

        # Verifies the contents of the preservation log for test_001, no-acc-num have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_001', 'no-acc-num', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.001', 'no-acc-num', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.001', 'no-acc-num', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.001', 'no-acc-num', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.001', 'no-acc-num', today, 'BLANK',
                     'Validated bag for accession no-acc-num. The bag is not valid. '
                     'Payload-Oxum validation failed. Expected 4 files and 43 bytes but found 1 files and 9 bytes',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, test_001/no-acc-num preservation log')

        # Verifies the contents of the preservation log for test_005, AC002_ER have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_005', 'AC002_ER', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.005', 'AC002.ER', '2023-10-03', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.005', 'AC002.ER', '2023-10-03', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.005', 'AC002.ER', '2023-10-04', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.005', 'AC002.ER', today, 'BLANK',
                     'Validated bag for accession AC002.ER. The bag is not valid. '
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, test_005/AC002_ER preservation log')

        # Verifies the contents of the preservation log for test_005, no-acc-num have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_005', 'no-acc-num', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.005', 'no-acc-num', '2023-10-03', 'CD.002', 'Copied.', 'Jane Doe'],
                    ['TEST.005', 'no-acc-num', '2023-10-03', 'BLANK', 'Bag valid.', 'Jane Doe'],
                    ['TEST.005', 'no-acc-num', today, 'BLANK',
                     'Validated bag for accession no-acc-num. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, test_005/no-acc-num preservation log')

        # Verifies the contents of the preservation log for test_123, AC001_ER have been updated.
        log_path = os.path.join(input_directory, 'closed', 'test_123', 'AC001_ER', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.123', 'AC001.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.123', 'AC001.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.123', 'AC001.ER', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.123', 'AC001.ER', today, 'BLANK',
                     'Validated bag for accession AC001.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for dup_accession, test_123/AC001_ER preservation log')

    def test_mix(self):
        """Test for when the script runs correctly on a mix of valid and not valid accessions,
        as well as an accession without a preservation log."""
        # Makes a copy of the preservation logs, since it will be updated by the test.
        accessions = [os.path.join('mix', 'born-digital', 'backlogged', 'test_001', '2023_test001_002_er'),
                      os.path.join('mix', 'born-digital', 'backlogged', 'test_001', '2023_test001_004_er'),
                      os.path.join('mix', 'born-digital', 'backlogged', 'test_005', '2023_test005_001_er')]
        for accession in accessions:
            shutil.copyfile(os.path.join('test_data', 'script', accession, 'preservation_log_copy.txt'),
                            os.path.join('test_data', 'script', accession, 'preservation_log.txt'))

        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script', 'mix', 'born-digital')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, capture_output=True, text=True)
        today = date.today().strftime('%Y-%m-%d')

        # # Verifies the script printed the correct message about the missing preservation log and validation errors.
        result = output.stdout
        expected = (f'Starting on accession {input_directory}\\backlogged\\test_001\\2023_test001_002_er (Bag)\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_001\\2023_test001_004_er (Bag)\n'
                    f'Starting on accession {input_directory}\\backlogged\\test_005\\2023_test005_001_er (Zipped_Bag)\n'
                    f'Starting on accession {input_directory}\\closed\\test_123\\2023_test123_001_er (Zip)\n'
                    '\nValidation errors found, see the fixity validation log in the input_directory.\n')
        self.assertEqual(expected, result, 'Problem with test for mix, printed message')

        # Verifies the contents of the fixity validation log are correct.
        result = csv_to_list(os.path.join(input_directory, f"fixity_validation_log_{today}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result'],
                    ['backlogged', 'test_001', '2023_test001_002_er',
                     os.path.join(input_directory, 'backlogged', 'test_001', '2023_test001_002_er'), 'Bag',
                     'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['backlogged', 'test_001', '2023_test001_004_er',
                     os.path.join(input_directory, 'backlogged', 'test_001', '2023_test001_004_er'), 'Bag',
                     'Updated', 'False', datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'Bag validation failed: data\\CD_2\\File2.txt md5 validation failed: '
                     'expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" found="85c8fbcb2ff1d73cb94ed9c355eb20d5"'],
                    ['backlogged', 'test_005', '2023_test005_001_er',
                     os.path.join(input_directory, 'backlogged', 'test_005', '2023_test005_001_er'), 'Zipped_Bag',
                     'Updated', 'False', datetime.now().strftime('%Y-%m-%d %H:%M'),
                     'Payload-Oxum validation failed. Expected 1 files and 589 bytes but found 2 files and 613 bytes'],
                    ['closed', 'test_123', '2023_test123_001_er',
                     os.path.join(input_directory, 'closed', 'test_123', '2023_test123_001_er'), 'Zip',
                     'Log path not found', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid']]
        self.assertEqual(expected, result, 'Problem with test for mix, validation report')

        # Verifies the contents of the preservation log for 2023_test001_002_er have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_001', '2023_test001_002_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.2.ER', today, 'BLANK',
                     'Validated bag for accession 2023.1.2.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for mix, 2023_test001_002_er preservation log')

        # Verifies the contents of the preservation log for 2023_test001_004_er have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_001', '2023_test001_004_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.4.ER', today, 'BLANK',
                     'Validated bag for accession 2023.1.4.ER. The bag is not valid. Bag validation failed: '
                     'data\\CD_2\\File2.txt md5 validation failed: expected="00a0aaaa0aa0a00ab00ad0a000aa00a0" '
                     'found="85c8fbcb2ff1d73cb94ed9c355eb20d5"', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for mix, 2023_test001_004_er preservation log')

        # Verifies the contents of the preservation log for 2023_test005_001_er have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'test_005', '2023_test005_001_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'CD.001', 'Copied.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'CD.002', 'Copied.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'BLANK', 'Zipped to bag.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', '2023-10-03', 'BLANK', 'Zipped bag valid.', 'Jane Doe'],
                    ['TEST.005', '2023.test005.001.ER', today, 'BLANK',
                     'Validated zip md5 for accession 2023.test005.001.ER. The zip is not valid. '
                     'Payload-Oxum validation failed. Expected 1 files and 589 bytes but found 2 files and 613 bytes',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for mix, 2023_test005_001_er preservation log')

    def test_restart(self):
        """Test for when the script is being restarted after a break
        and uses a pre-existing fixity validation log where some accessions already have a validation result"""
        # Makes a copy of the preservation logs, since it will be updated by the test.
        accessions = [os.path.join('restart', 'born-digital', 'backlogged', 'coll_2023', '2023_test004_002_er'),
                      os.path.join('restart', 'born-digital', 'backlogged', 'coll_2023', '2023_test005_004_er')]
        for accession in accessions:
            shutil.copyfile(os.path.join('test_data', 'script', accession, 'preservation_log_copy.txt'),
                            os.path.join('test_data', 'script', accession, 'preservation_log.txt'))

        # Makes the fixity validation log, as if the first two accessions had validated when running the script earlier.
        # It is made by the test instead of stored in the repo so the date in the filename will be correct.
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script', 'restart', 'born-digital')
        coll_path = os.path.join(input_directory, 'backlogged', 'coll_2023')
        rows = [['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result'],
                ['backlogged', 'coll_2023', '2023_test001_001_er', os.path.join(coll_path, '2023_test001_001_er'),
                 'Bag', 'Updated', 'True', '2000-01-01 12:12', 'Valid'],
                ['backlogged', 'coll_2023', '2023_test001_005_er', os.path.join(coll_path, '2023_test001_005_er'),
                 'Bag', 'Updated', 'False', '2000-01-01 12:13', 'Bag validation failed'],
                ['backlogged', 'coll_2023', '2023_test004_002_er', os.path.join(coll_path, '2023_test004_002_er'),
                 'Zip', None, None, None, None],
                ['backlogged', 'coll_2023', '2023_test005_004_er', os.path.join(coll_path, '2023_test005_004_er'),
                 'Zipped_Bag', None, None, None, None]]
        log_path = os.path.join(input_directory, f"fixity_validation_log_{date.today().strftime('%Y-%m-%d')}.csv")
        with open(log_path, 'w', newline='') as open_log:
            log_writer = csv.writer(open_log)
            log_writer.writerows(rows)

        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'validate_fixity.py')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, capture_output=True, text=True)
        today = date.today().strftime('%Y-%m-%d')

        # Verifies the script printed the correct message about validation errors.
        result = output.stdout
        expected = (f'Starting on accession {coll_path}\\2023_test004_002_er (Zip)\n'
                    f'Starting on accession {coll_path}\\2023_test005_004_er (Zipped_Bag)\n'
                    '\nValidation errors found, see the fixity validation log in the input_directory.\n')
        self.assertEqual(expected, result, 'Problem with test for restart, printed message')

        # Verifies the contents of the fixity validation log are correct.
        result = csv_to_list(os.path.join(input_directory, f"fixity_validation_log_{today}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result'],
                    ['backlogged', 'coll_2023', '2023_test001_001_er', os.path.join(coll_path, '2023_test001_001_er'),
                     'Bag', 'Updated', 'True', '2000-01-01 12:12', 'Valid'],
                    ['backlogged', 'coll_2023', '2023_test001_005_er', os.path.join(coll_path, '2023_test001_005_er'),
                     'Bag', 'Updated', 'False', '2000-01-01 12:13', 'Bag validation failed'],
                    ['backlogged', 'coll_2023', '2023_test004_002_er', os.path.join(coll_path, '2023_test004_002_er'),
                     'Zip', 'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['backlogged', 'coll_2023', '2023_test005_004_er', os.path.join(coll_path, '2023_test005_004_er'),
                     'Zipped_Bag', 'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid']]
        self.assertEqual(expected, result, 'Problem with test for restart, fixity validation log')

        # Verifies the contents of the preservation log for 2023_test004_002_er have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'coll_2023', '2023_test004_002_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied, no errors.', 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'BLANK', "Can't bag; made zip.", 'JD'],
                    ['T4', '2023.T4.02.ER', '2023-10-03', 'BLANK', 'Validated zip. Valid.', 'JD'],
                    ['T4', '2023.T4.02.ER', today, 'BLANK',
                     'Validated zip for accession 2023.T4.02.ER. The zip is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for restart, 2023_test004_002_er preservation log')

        # Verifies the contents of the preservation log for 2023_test005_004_er have been updated.
        log_path = os.path.join(input_directory, 'backlogged', 'coll_2023', '2023_test005_004_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.1', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'CD.2', 'Virus scanned and copied. No errors.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'BLANK', 'Zipped to bag.', 'JD'],
                    ['T5', '2023.T5.04.ER', '2023-10-03', 'BLANK', 'Zipped bag valid.', 'JD'],
                    ['T5', '2023.T5.04.ER', today, 'BLANK',
                     'Validated zipped_bag for accession 2023.T5.04.ER. The zipped_bag is valid.',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for restart, 2023_test005_004_er preservation log')

    def test_valid(self):
        """Test for when the script runs correctly and both accessions are valid
        There are also a folder and file that the script should skip
        and accession 2023_test001_001_er contains a manifest that the script should skip as well as being in a bag.
        """
        # Makes a copy of the preservation logs, since it will be updated by the test.
        accessions = [os.path.join('valid', 'Born-digital', 'closed', 'test_001', '2023_test001_001_er'),
                      os.path.join('valid', 'Born-digital', 'closed', 'test_004', '2023_test004_003_er')]
        for accession in accessions:
            shutil.copyfile(os.path.join('test_data', 'script', accession, 'preservation_log_copy.txt'),
                            os.path.join('test_data', 'script', accession, 'preservation_log.txt'))
            
        # Makes the variables used for script input and runs the script.
        script = os.path.join(os.getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = os.path.join(os.getcwd(), 'test_data', 'script', 'valid', 'Born-digital')
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, capture_output=True, text=True)
        today = date.today().strftime('%Y-%m-%d')

        # Verifies the script printed the correct message about validation errors.
        result = output.stdout
        status_path = os.path.join(input_directory, 'closed')
        expected = (f'Starting on accession {status_path}\\test_001\\2023_test001_001_er (Bag)\n'
                    f'Starting on accession {status_path}\\test_004\\2023_test004_003_er (Zipped_Bag)\n'
                    '\nNo validation errors.\n')
        self.assertEqual(expected, result, 'Problem with test for valid, printed message')

        # Verifies the contents of the fixity validation log.
        result = csv_to_list(os.path.join(input_directory, f"fixity_validation_log_{today}.csv"))
        expected = [['Status', 'Collection', 'Accession', 'Path', 'Fixity_Type', 'Pres_Log', 'Valid', 'Valid_Time', 'Result'],
                    ['closed', 'test_001', '2023_test001_001_er',
                     os.path.join(input_directory, 'closed', 'test_001', '2023_test001_001_er'), 'Bag',
                     'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'test_004', '2023_test004_003_er',
                     os.path.join(input_directory, 'closed', 'test_004', '2023_test004_003_er'), 'Zipped_Bag',
                     'Updated', 'True', datetime.now().strftime('%Y-%m-%d %H:%M'), 'Valid'],
                    ['closed', 'to_skip', 'to_skip', os.path.join(input_directory, 'closed', 'to_skip', 'to_skip'),
                    'BLANK', 'BLANK', 'Skipped', 'BLANK', 'Not an accession']]
        self.assertEqual(expected, result, 'Problem with test for valid, fixity validation log')

        # Verifies the contents of the preservation log for 2023_test001_001_er have been updated.
        log_path = os.path.join(input_directory, 'closed', 'test_001', '2023_test001_001_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.001', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-30', 'CD.002', 'Copied with no errors.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', '2023-10-31', 'BLANK', 'Made bag. The bag is valid.', 'Jane Doe'],
                    ['TEST.1', '2023.1.1.ER', today, 'BLANK',
                     'Validated bag for accession 2023.1.1.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for valid, 2023_test001_001_er preservation log')

        # Verifies the contents of the preservation log for 2023_test004_003_er have been updated.
        log_path = os.path.join(input_directory, 'closed', 'test_004', '2023_test004_003_er', 'preservation_log.txt')
        result = csv_to_list(log_path, delimiter='\t')
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'CD.001', 'Copied.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'CD.002', 'Copied.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'BLANK', 'Zipped to bag.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', '2023-11-24', 'BLANK', 'Zipped bag valid.', 'Jane Doe'],
                    ['TEST.004', '2023.test004.003.ER', today, 'BLANK',
                     'Validated zipped_bag for accession 2023.test004.003.ER. The zipped_bag is valid.',
                     'validate_fixity.py']]
        self.assertEqual(expected, result, 'Problem with test for valid, 2023_test004_003_er preservation log')

    def test_arg_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = os.path.join(os.getcwd(), '..', '..', 'validate_fixity.py')
        input_directory = os.path.join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{input_directory}"', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python "{script}" "{input_directory}"', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided input_directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(expected, result, 'Problem with test for script argument error, printed error')


if __name__ == '__main__':
    unittest.main()
