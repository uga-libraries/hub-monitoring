"""
Tests for the function files_per_format(), which gets the number of files per format name/version/risk combination.
To simplify the test input, tests only have the columns needed for that test.
"""
import unittest
from format_list import files_per_format
from test_df_cleanup import df_to_list
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def test_repeats_combined(self):
        """Test for combining repeating name, version, risk combinations (all three match)"""
        df_formats = DataFrame([['path1', 'format1', 'v1', 111, 'Moderate Risk'],
                                ['path2', 'format1', 'v1', 112, 'Moderate Risk'],
                                ['path3', 'format1', 'v2', 221, 'Low Risk'],
                                ['path4', 'format1', 'v2', 222, 'Low Risk'],
                                ['path5', 'format1', 'v2', 331, 'No Match'],
                                ['path6', 'format1', 'v2', 332, 'No Match'],
                                ['path7', 'format1', 'v2', 333, 'No Match']],
                               columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                        'NARA_Risk_Level'])
        df_files = files_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count'],
                    ['format1', 'v1', 'Moderate Risk', 2],
                    ['format1', 'v2', 'Low Risk', 2],
                    ['format1', 'v2', 'No Match', 3]]
        self.assertEqual(expected, result, "Problem with test for repeats combined")

    def test_repeats_not_combined(self):
        """Test for not combining repeating name, version, and/or risk combinations (all three don't match)"""
        df_formats = DataFrame([['path/format-only/1', 'format1', 'v1', 1, 'Moderate Risk'],
                                ['path/format-only/2', 'format1', 'v2', 1, 'High Risk'],
                                ['path/version-only/1', 'format2', 'v3', 2, 'Moderate Risk'],
                                ['path/version-only/2', 'format3', 'v3', 2, 'Low Risk'],
                                ['path/risk-only/1', 'format4', 'v4', 3, 'Low Risk'],
                                ['path/risk-only/2', 'format5', 'v5', 3, 'Low Risk'],
                                ['path/format-version/1', 'format6', 'v6', 4, 'Low Risk'],
                                ['path/format-version/2', 'format6', 'v6', 4, 'No Match'],
                                ['path/format-risk/1', 'format7', 'v7', 5, 'No Match'],
                                ['path/format-risk/2', 'format7', 'v8', 5, 'No Match'],
                                ['path/version-risk/1', 'format8', 'v9', 6, 'Moderate Risk'],
                                ['path/version-risk/2', 'format9', 'v9', 6, 'Moderate Risk']],
                               columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                        'NARA_Risk_Level'])
        df_files = files_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count'],
                    ['format1', 'v1', 'Moderate Risk', 1],
                    ['format1', 'v2', 'High Risk', 1],
                    ['format2', 'v3', 'Moderate Risk', 1],
                    ['format3', 'v3', 'Low Risk', 1],
                    ['format4', 'v4', 'Low Risk', 1],
                    ['format5', 'v5', 'Low Risk', 1],
                    ['format6', 'v6', 'Low Risk', 1],
                    ['format6', 'v6', 'No Match', 1],
                    ['format7', 'v7', 'No Match', 1],
                    ['format7', 'v8', 'No Match', 1],
                    ['format8', 'v9', 'Moderate Risk', 1],
                    ['format9', 'v9', 'Moderate Risk', 1]]
        self.assertEqual(expected, result, "Problem with test for repeats not combined")

    def test_unique(self):
        """Test for not combining unique name, version, risk combinations (none of the three match)"""
        df_formats = DataFrame([['path1', 'format1', 'v1', 1, 'High Risk'],
                                ['path2', 'format2', 'v2', 2, 'Moderate Risk'],
                                ['path3', 'format3', 'v3', 3, 'Low Risk'],
                                ['path4', 'format4', 'v4', 4, 'No Match']],
                               columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                        'NARA_Risk_Level'])
        df_files = files_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'File_Count'],
                    ['format1', 'v1', 'High Risk', 1],
                    ['format2', 'v2', 'Moderate Risk', 1],
                    ['format3', 'v3', 'Low Risk', 1],
                    ['format4', 'v4', 'No Match', 1]]
        self.assertEqual(expected, result, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
