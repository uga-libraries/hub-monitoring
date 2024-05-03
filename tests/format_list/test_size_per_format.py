"""
Test for the function size_per_format(), which gets the GB per format name/version/risk combination.
"""
import unittest
from format_list import combine_risk_csvs, df_cleanup, size_per_format
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        directory = join(getcwd(), 'test_data')
        df_all = combine_risk_csvs(directory)
        df_formats = df_cleanup(df_all)
        df_size = size_per_format(df_formats)

        df = df_size.fillna('nan')
        result = [df.columns.tolist()] + df.values.tolist()
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'Size_GB'],
                    ['JPEG File Interchange Format', '1.01', 'Low Risk', 82.858],
                    ['JPEG File Interchange Format', '1.02', 'Low Risk', 0.183],
                    ['PDF/A', '1b', 'Low Risk', 45.837],
                    ['Plain text', 'nan', 'Moderate Risk', 5.113],
                    ['Portable Document Format', '1.4', 'Moderate Risk', 0.504],
                    ['Portable Network Graphics', '1', 'High Risk', 205.688],
                    ['Portable Network Graphics', '1', 'Moderate Risk', 257.638],
                    ['Unknown Binary', 'nan', 'No Match', 0.0]]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
