"""
Test for the function cleanup(), which transforms the full dataframe into a dataframe with select format information.
"""
import unittest
from format_list import combine_risk_csvs, df_cleanup
from os import getcwd
from os.path import join


def df_to_list(df):
    """Convert a dataframe to a list of list, with the column names and row values
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = df.fillna('nan')
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_space(self):
        """Test for when the NARA risk column is named NARA_Risk Level"""
        input_directory = join(getcwd(), 'test_data_space')
        df_all = combine_risk_csvs(input_directory)
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['Portable Document Format', '1.4', 410000.486, 'Moderate Risk'],
                    ['JPEG File Interchange Format', '1.01', 220000.139, 'Low Risk'],
                    ['JPEG File Interchange Format', '1.02', 183000.783, 'Low Risk'],
                    ['Portable Document Format', '1.4', 94000.626, 'Moderate Risk'],
                    ['JPEG File Interchange Format', '1.02', 110.597, 'Low Risk'],
                    ['JPEG File Interchange Format', '1.02', 95.086, 'Low Risk'],
                    ['Unknown Binary', 'no-version', 195.06, 'No Match'],
                    ['JPEG File Interchange Format', '1.01', 82638000.0, 'Low Risk'],
                    ['Portable Network Graphics', '1', 257638000.0, 'Moderate Risk'],
                    ['Portable Network Graphics', '1', 205688000.0, 'High Risk'],
                    ['Plain text', 'no-version', 5113000.0, 'Moderate Risk'],
                    ['PDF/A', '1b', 45837000.0, 'Low Risk']]
        self.assertEqual(result, expected, "Problem with test for space")

    def test_underscore(self):
        """Test for when the NARA risk column is named NARA_Risk_Level"""
        input_directory = join(getcwd(), 'test_data_underscore')
        df_all = combine_risk_csvs(input_directory)
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['Portable Document Format', '1.4', 410000.486, 'Moderate Risk'],
                    ['JPEG File Interchange Format', '1.01', 220000.139, 'Low Risk'],
                    ['JPEG File Interchange Format', '1.02', 183000.783, 'Low Risk'],
                    ['Portable Document Format', '1.4', 94000.626, 'Moderate Risk'],
                    ['JPEG File Interchange Format', '1.02', 110.597, 'Low Risk'],
                    ['JPEG File Interchange Format', '1.02', 95.086, 'Low Risk'],
                    ['Unknown Binary', 'no-version', 195.06, 'No Match'],
                    ['JPEG File Interchange Format', '1.01', 82638000.0, 'Low Risk'],
                    ['Portable Network Graphics', '1', 257638000.0, 'Moderate Risk'],
                    ['Portable Network Graphics', '1', 205688000.0, 'High Risk'],
                    ['Plain text', 'no-version', 5113000.0, 'Moderate Risk'],
                    ['PDF/A', '1b', 45837000.0, 'Low Risk']]
        self.assertEqual(result, expected, "Problem with test for underscore")


if __name__ == '__main__':
    unittest.main()
