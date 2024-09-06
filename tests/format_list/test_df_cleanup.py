"""
Tests for the function df_cleanup(), which transforms the full dataframe into a dataframe with
select columns, no duplicates, and does some reformatting.

To simplify the test input, tests have the columns needed for that test.
"""
import unittest
from format_list import df_cleanup
from numpy import nan
from pandas import DataFrame


def df_to_list(df):
    """Convert a dataframe to a list of list, with the column names and row values
    Blanks are filled with a string because np.nan comparisons work inconsistently.
    """
    df = df.fillna('nan')
    df_list = [df.columns.tolist()] + df.values.tolist()
    return df_list


class MyTestCase(unittest.TestCase):

    def test_all_columns(self):
        """Test expected columns are dropped"""
        # Makes the dataframe of combined risk data. This is the only test with all columns.
        df_all = DataFrame([['path1', 'format1', 'v1', 'puid1', 'tool1', False, '2024-09-06', 111, 'md51', 'app1',
                             True, True, 'note1', 'nara1', 'ext1', 'puid1', 'Low Risk', 'Retain', 'PUID',
                             'Not for TA', 'Not for Other'],
                            ['path2', 'format2', 'v2', 'puid2', 'tool2', False, '2024-09-06', 222, 'md52', 'app2',
                             True, True, 'note2', 'nara2', 'ext2', 'puid2', 'High Risk', 'Retain', 'PUID',
                             'Not for TA', 'Not for Other']],
                           columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                                    'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified',
                                    'FITS_Size_KB', 'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid',
                                    'FITS_Well-Formed', 'FITS_Status_Message', 'NARA_Format Name',
                                    'NARA_File Extension(s)', 'NARA_PRONOM URL', 'NARA_Risk_Level',
                                    'NARA_Proposed Preservation Plan', 'NARA_Match_Type', 'Technical_Appraisal',
                                    'Other_Risk'])
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['format1', 'v1', 111, 'Low Risk'],
                    ['format2', 'v2', 222, 'High Risk']]
        self.assertEqual(result, expected, "Problem with test for all columns")

    def test_duplicates(self):
        """Test duplicates of files with the same NARA risk level"""
        # Makes the dataframe of combined risk data with just the columns needed for this test.
        df_all = DataFrame([['path1', 'format1', 'v1', 111, 'Low Risk'],
                            ['path1', 'format1', 'v1', 111, 'Moderate Risk'],
                            ['path1', 'format1', 'v1', 111, 'Low Risk'],
                            ['path2', 'format1', 'v1', 222, 'Low Risk']],
                           columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                    'NARA_Risk_Level'])
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['format1', 'v1', 111, 'Low Risk'],
                    ['format1', 'v1', 111, 'Moderate Risk'],
                    ['format1', 'v1', 222, 'Low Risk']]
        self.assertEqual(result, expected, "Problem with test for duplicates")

    def test_nara_blank(self):
        """Test filling blank NARA risk level with No Match"""
        # Makes the dataframe of combined risk data with just the columns needed for this test.
        df_all = DataFrame([['path1', 'format1', 'v1', 111, nan],
                            ['path2', 'format2', 'v2', 222, nan]],
                           columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                    'NARA_Risk_Level'])
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['format1', 'v1', 111, 'No Match'],
                    ['format2', 'v2', 222, 'No Match']]
        self.assertEqual(result, expected, "Problem with test for NARA blank risk level")

    def test_nara_rename(self):
        """Test renaming NARA_Risk Level to NARA_Risk_Level"""
        # Makes the dataframe of combined risk data with just the columns needed for this test.
        df_all = DataFrame([['path1', 'format1', 'v1', 111, nan]],
                           columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                    'NARA_Risk Level'])
        df_formats = df_cleanup(df_all)

        result = df_to_list(df_formats)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB', 'NARA_Risk_Level'],
                    ['format1', 'v1', 111, 'No Match']]
        self.assertEqual(result, expected, "Problem with test for NARA rename risk level")


if __name__ == '__main__':
    unittest.main()
