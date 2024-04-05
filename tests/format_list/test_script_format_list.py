"""
Test for the script format_list.py
"""
import unittest
from os import getcwd, remove
from os.path import exists, join
from pandas import read_csv
from subprocess import run


class MyTestCase(unittest.TestCase):

    def tearDown(self):
        """Delete script output, if created"""
        output = join('test_data', 'combined_format_data.csv')
        if exists(output):
            remove(output)

    def test_script(self):
        script = join(getcwd(), '..', '..', 'format_list.py')
        run(f'python {script} test_data', shell=True)

        df = read_csv(join('test_data', 'combined_format_data.csv'))
        df = df.fillna('nan')
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count', 'Size_GB'],
                    ['JPEG File Interchange Format', '1.01', 'Low Risk', 2, 82.858],
                    ['JPEG File Interchange Format', '1.02', 'Low Risk', 3, 0.183],
                    ['PDF/A', '1b', 'Low Risk', 1, 45.837],
                    ['Plain text', 'nan', 'Moderate Risk', 1, 5.113],
                    ['Portable Document Format', '1.4', 'Moderate Risk', 2, 0.504],
                    ['Portable Network Graphics', '1', 'High Risk', 1, 205.688],
                    ['Portable Network Graphics', '1', 'Moderate Risk', 1, 257.638],
                    ['Unknown Binary', 'nan', 'No Match', 1, 0.0]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
