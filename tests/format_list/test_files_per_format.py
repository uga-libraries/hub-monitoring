"""
Test for the function files_per_format(), which gets the number of files per format name/version/risk combination.
"""
import unittest
from format_list import combine_risk_csvs, df_cleanup, files_per_format
from test_df_cleanup import df_to_list
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        input_directory = join(getcwd(), 'test_data')
        df_all = combine_risk_csvs(input_directory)
        df_formats = df_cleanup(df_all)
        df_files = files_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count'],
                    ['JPEG File Interchange Format', '1.01', 'Low Risk', 2],
                    ['JPEG File Interchange Format', '1.02', 'Low Risk', 3],
                    ['PDF/A', '1b', 'Low Risk', 1],
                    ['Plain text', 'no-version', 'Moderate Risk', 1],
                    ['Portable Document Format', '1.4', 'Moderate Risk', 2],
                    ['Portable Network Graphics', '1', 'High Risk', 1],
                    ['Portable Network Graphics', '1', 'Moderate Risk', 1],
                    ['Unknown Binary', 'no-version', 'No Match', 1]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
