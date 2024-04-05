"""
Test for the function cleanup(), which transforms the full dataframe into a dataframe with select format information.
"""
import unittest
from format_list import combine_risk_csvs, df_cleanup
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        df_all = combine_risk_csvs(join(getcwd(), 'test_data'))
        df_formats = df_cleanup(df_all)

        df_formats = df_formats.fillna('nan')
        result = [df_formats.columns.tolist()] + df_formats.values.tolist()
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['Portable Document Format', 1.4, 410000.486, 'Moderate Risk'],
                    ['JPEG File Interchange Format', 1.01, 220000.139, 'Low Risk'],
                    ['JPEG File Interchange Format', 1.02, 183000.783, 'Low Risk'],
                    ['Portable Document Format', 1.4, 94000.626, 'Moderate Risk'],
                    ['JPEG File Interchange Format', 1.02, 110.597, 'Low Risk'],
                    ['JPEG File Interchange Format', 1.02, 95.086, 'Low Risk'],
                    ['Unknown Binary', 'nan', 195.06, 'No Match'],
                    ['JPEG File Interchange Format', '1.01', 82638000.0, 'Low Risk'],
                    ['Portable Network Graphics', '1', 257638000.0, 'Moderate Risk'],
                    ['Portable Network Graphics', '1', 205688000.0, 'High Risk'],
                    ['Plain text', 'nan', 5113000.0, 'Moderate Risk'],
                    ['PDF/A', '1b', 45837000.0, 'Low Risk']]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
