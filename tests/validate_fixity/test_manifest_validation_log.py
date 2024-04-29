"""
Test for the function manifest_validation_log(), which saves validation errors to a text file.
"""
import unittest
from validate_fixity import manifest_validation_log
from os import getcwd, remove
from os.path import basename, exists, join
from pandas import read_csv


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Deletes the validation report, if made by the test."""
        report = join(getcwd(), 'test_data', 'test_005_manifest_invalid',
                      '2023_test005_001_er_manifest_validation_errors.csv')
        if exists(report):
            remove(report)

    def test_function(self):
        """Test for correct operation of the function"""
        # Makes variables for function input and runs the function.
        directory = join('test_data', 'test_005_manifest_invalid')
        root = join(directory, '2023_test005_001_er')
        errors_list = [['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                       ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                       [join(root, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                       [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        manifest_validation_log(directory, basename(root), errors_list)

        # Verifies the report has the correct values.
        df = read_csv(join(directory, '2023_test005_001_er_manifest_validation_errors.csv'))
        report_rows = [df.columns.tolist()] + df.values.tolist()
        expected = [['File', 'MD5', 'MD5_Source'],
                    ['Z:\\2023_test005_002_er\\CD_2\\File02.txt', '0CBC6611F5540BD0809A388DC95A615B', 'Manifest'],
                    ['Z:\\2023_test005_002_er\\CD_1\\File1.txt', '4324B4C675E56A5E04BD9A8C74796EE5', 'Manifest'],
                    [join(root, 'CD_1', 'File1.txt'), '717216B472AA04EB2E615809C7F30C4E', 'Current'],
                    [join(root, 'CD_2', 'File02.txt'), '8078CD550FCF6755750A59378AFC7D30', 'Current']]
        self.assertEqual(report_rows, expected)


if __name__ == '__main__':
    unittest.main()
