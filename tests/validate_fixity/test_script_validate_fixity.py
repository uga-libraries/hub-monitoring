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


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Return the preservation logs to the original contents after testing,
        using a copy of the original log that is also in the accession folder,
        and delete reports made by the script."""
        # Preservation logs
        bag_accessions = ['2023_test001_001_er', '2023_test001_002_er']
        for bag_accession in bag_accessions:
            folder = join(getcwd(), 'test_data', 'test_001_bags_valid', bag_accession)
            copyfile(join(folder, 'preservation_log_copy.txt'), join(folder, 'preservation_log.txt'))

        accessions = ['2023_test003_001_er', '2023_test003_002_er', '2023_test003_003_er', '2023_test003_004_er']
        for accession in accessions:
            folder = join(getcwd(), 'test_data','test_003_log_update', accession)
            copyfile(join(folder, 'preservation_log_copy.txt'), join(folder, 'preservation_log.txt'))

        # Reports
        directory = join(getcwd(), 'test_data', 'test_003_log_update')
        reports = [f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv",
                   '2023_test003_003_er_manifest_validation_errors.csv']
        for report in reports:
            if exists(join(directory, report)):
                remove(join(directory, report))

        # Report that should not be made, since the bag accessions are valid.
        bag_report = join(getcwd(), 'test_data', 'test_001_bags_valid',
                          f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
        if exists(bag_report):
            remove(bag_report)

    def test_correct_errors(self):
        """Test for when the script runs correctly on all accessions in collection test_003.
        It includes 2 accessions with validation errors and three that validate."""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), 'test_data', 'test_003_log_update')
        msg = subprocess.run(f'python "{script}" "{directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about the missing preservation log and validation errors.
        result = msg.stdout.decode('utf-8')
        expected = ('\r\nERROR: accession 2023_test003_005_er has no preservation log.\r\n'
                    '\r\nValidation errors found, see fixity_validation.csv in the directory '
                    'provided as the script argument.\r\n')
        self.assertEqual(result, expected, 'Problem with test for correct, printed message')

        # Verifies the contents of the validation report are correct.
        df = read_csv(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        df = df.fillna('nan')
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors'],
                    ['2023_test003_001_er_bag', False,
                     'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes'],
                    ['2023_test003_002_er_bag', True, 'nan'],
                    ['2023_test003_003_er', False, '6 errors'],
                    ['2023_test003_004_er', True, '0 errors'],
                    ['2023_test003_005_er', True, '0 errors']]
        self.assertEqual(report_rows, expected, 'Problem with test for correct, validation report')

        # Verifies the contents of the log for 2023_test003_001_er have been updated.
        df = read_csv(join(directory, '2023_test003_001_er', 'preservation_log.txt'), delimiter='\t')
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
                     'Validated bag for accession 2023.3.1.ER. The bag is not valid. Payload-Oxum validation failed. '
                     'Expected 1 files and 4 bytes but found 1 files and 26 bytes', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_001_er')

        # Verifies the contents of the log for 2023_test003_002_er have been updated.
        df = read_csv(join(directory, '2023_test003_002_er', 'preservation_log.txt'), delimiter='\t')
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
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_002_er')

        # Verifies the contents of the log for 2023_test003_003_er have been updated.
        df = read_csv(join(directory, '2023_test003_003_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', '2023-03-28', 'nan', 'Cannot bag. Made manifest. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.3.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.3.ER. The manifest is not valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_003_er')

        # Verifies the contents of 2023_test0003_004_er manifest validation errors log.
        df = read_csv(join(directory, '2023_test003_003_er_manifest_validation_errors.csv'))
        rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\CD_2\\File03.txt', '3D77C578A138BA560F31DD22B83A53D3', 'Manifest'],
                    ['Z:\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(directory, '2023_test003_003_er', '2023_test003_003_er', 'CD_1', 'File1.txt'),
                     '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                    [join(directory, '2023_test003_003_er', '2023_test003_003_er', 'CD_2', 'File02.txt'),
                     '8078CD550FCF6755750A59378AFC7D30', 'Current'],
                    [join(directory, '2023_test003_003_er', '2023_test003_003_er','CD_1', 'New Text Document.txt'),
                     '9669CD9006F03AD6F1F8831601640482', 'Current']]
        self.assertEqual(rows, expected, 'Problem with test for correct, manifest validation errors')

        # Verifies the contents of the log for 2023_test003_004_er have been updated.
        df = read_csv(join(directory, '2023_test003_004_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD1', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD1', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD2', 'Virus scanned. No threats.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'CD2', 'Copied. No errors.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', '2023-04-28', 'nan', 'Cannot bag. Made manifest. Valid.', 'Jane Doe'],
                    ['TEST.3', '2023.3.4.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated manifest for accession 2023.3.4.ER. The manifest is valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct, 2023_test003_004_er')

    def test_correct_no_errors(self):
        """Test for when the script runs correctly on all accessions in collection test_001.
        It includes 2 accessions, both bags, that validate."""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), 'test_data', 'test_001_bags_valid')
        msg = subprocess.run(f'python "{script}" "{directory}"', shell=True, stdout=subprocess.PIPE)

        # Verifies the script printed the correct message about validation errors.
        result = msg.stdout.decode('utf-8')
        expected = '\r\nNo validation errors.\r\n'
        self.assertEqual(result, expected, 'Problem with test for correct no errors, printed message')

        # Verifies the validation report was not made. It is only made for errors.
        report_path = join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv")
        report_made = exists(report_path)
        self.assertEqual(report_made, False, 'Problem with test for correct no errors, validation report')

        # Verifies the contents of the log for 2023_test001_001_er have been updated.
        df = read_csv(join(directory, '2023_test001_001_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-30', 'CD.001',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-30', 'CD.001',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-30', 'CD.001',
                     'Bagged with accession 2023.test001.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-31', 'CD.002',
                     'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-31', 'CD.002',
                     'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-31', 'CD.002',
                     'Bagged with accession 2023.test001.001.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', '2023-10-31', 'nan',
                     'Validated bag for accession 2023.test001.001.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.001.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test001.001.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct no errors, 2023_test001_001_er')

        # Verifies the contents of the log for 2023_test001_002_er have been updated.
        df = read_csv(join(directory, '2023_test001_002_er', 'preservation_log.txt'), delimiter='\t')
        df = df.fillna('nan')
        log_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Collection', 'Accession', 'Date', 'Media Identifier', 'Action', 'Staff'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001', 'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001', 'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-14', 'CD.001', 'Bagged with accession 2023.test001.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002', 'Virus scanned using Microsoft Defender. No security threats were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002', 'Copied to external storage device using TeraCopy. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'CD.002', 'Bagged with accession 2023.test001.002.ER. No errors were detected.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', '2023-11-15', 'nan', 'Validated bag for accession 2023.test001.002.ER. The bag was valid.', 'Jane Doe'],
                    ['TEST.001', '2023.test001.002.ER', date.today().strftime('%Y-%m-%d'), 'nan',
                     'Validated bag for accession 2023.test001.002.ER. The bag is valid.', 'validate_fixity.py']]
        self.assertEqual(log_rows, expected, 'Problem with test for correct no errors, 2023_test003_002_er')

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python "{script}" "{directory}"', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python {script} {directory}', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, 'Problem with test for printed error')


if __name__ == '__main__':
    unittest.main()
