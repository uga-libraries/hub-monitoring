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

    def test_correct(self):
        """Test for when the script runs correctly on all accessions in Validate_Fixity_Hub, collection test_003"""
        # Makes the variables used for script input and runs the script.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join(getcwd(), 'test_data', 'test_003_log_update')
        subprocess.run(f'python {script} {directory}', shell=True)

        # Verifies the contents of the validation report are correct.
        df = read_csv(join(directory, f"fixity_validation_{date.today().strftime('%Y-%m-%d')}.csv"))
        df = df.fillna('nan')
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['Accession', 'Valid', 'Errors'],
                    ['2023_test003_001_er_bag', False,
                     'Payload-Oxum validation failed. Expected 1 files and 4 bytes but found 1 files and 26 bytes'],
                    ['2023_test003_002_er_bag', True, 'nan'],
                    ['2023_test003_003_er', False, '6 errors'],
                    ['2023_test003_004_er', True, '0 errors']]
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
                     'Validated bag for accession 2023.3.1.ER. The bag is not valid.', 'validate_fixity.py']]
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

    def test_error(self):
        """Test for when the script argument is not correct and the script exits"""
        # Makes the variables used for script input.
        # The script will be run twice in this test.
        script = join(getcwd(), '..', '..', 'validate_fixity.py')
        directory = join('test_data', 'Error')

        # Runs the script and tests that it exits.
        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.run(f'python {script} {directory}', shell=True, check=True, stdout=subprocess.PIPE)

        # Runs the script a second time and tests that it prints the correct error.
        output = subprocess.run(f'python {script} {directory}', shell=True, stdout=subprocess.PIPE)
        result = output.stdout.decode('utf-8')
        expected = "Provided directory 'test_data\\Error' does not exist\r\n"
        self.assertEqual(result, expected, "Problem with test for printed error")


if __name__ == '__main__':
    unittest.main()
