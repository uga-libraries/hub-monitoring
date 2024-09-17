"""
Test for the function size_per_format(), which gets the GB per format name/version/risk combination.
To simplify the test input, tests only have the columns needed for that test.
"""
import unittest
from format_list import size_per_format
from test_df_cleanup import df_to_list
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def test_repeats_not_combined(self):
        """Test for not combining repeating name, version, and/or risk combinations (all three don't match)"""
        df_formats = DataFrame([['path/format-only/1', 'format1', 'v1', 1000000, 'Moderate Risk'],
                                ['path/format-only/2', 'format1', 'v2', 2000000, 'High Risk'],
                                ['path/version-only/1', 'format2', 'v3', 3000000, 'Moderate Risk'],
                                ['path/version-only/2', 'format3', 'v3', 4000000, 'Low Risk'],
                                ['path/risk-only/1', 'format4', 'v4', 5000000, 'Low Risk'],
                                ['path/risk-only/2', 'format5', 'v5', 6000000, 'Low Risk'],
                                ['path/format-version/1', 'format6', 'v6', 7000000, 'Low Risk'],
                                ['path/format-version/2', 'format6', 'v6', 8000000, 'No Match'],
                                ['path/format-risk/1', 'format7', 'v7', 9000000, 'No Match'],
                                ['path/format-risk/2', 'format7', 'v8', 10000000, 'No Match'],
                                ['path/version-risk/1', 'format8', 'v9', 11000000, 'Moderate Risk'],
                                ['path/version-risk/2', 'format9', 'v9', 12000000, 'Moderate Risk']],
                               columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                        'NARA_Risk_Level'])
        df_files = size_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'Size_GB'],
                    ['format1', 'v1', 'Moderate Risk', 1.0],
                    ['format1', 'v2', 'High Risk', 2.0],
                    ['format2', 'v3', 'Moderate Risk', 3.0],
                    ['format3', 'v3', 'Low Risk', 4.0],
                    ['format4', 'v4', 'Low Risk', 5.0],
                    ['format5', 'v5', 'Low Risk', 6.0],
                    ['format6', 'v6', 'Low Risk', 7.0],
                    ['format6', 'v6', 'No Match', 8.0],
                    ['format7', 'v7', 'No Match', 9.0],
                    ['format7', 'v8', 'No Match', 10.0],
                    ['format8', 'v9', 'Moderate Risk', 11.0],
                    ['format9', 'v9', 'Moderate Risk', 12.0]
                    ]
        self.assertEqual(result, expected, "Problem with test for repeats not combined")

    def test_unique(self):
        """Test for not combining unique name, version, risk combinations (none of the three match)"""
        df_formats = DataFrame([['path1', 'format1', 'v1', 1000000, 'High Risk'],
                                ['path2', 'format2', 'v2', 2000000, 'Moderate Risk'],
                                ['path3', 'format3', 'v3', 3000000, 'Low Risk'],
                                ['path4', 'format4', 'v4', 4000000, 'No Match']],
                               columns=['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_Size_KB',
                                        'NARA_Risk_Level'])
        df_files = size_per_format(df_formats)

        result = df_to_list(df_files)
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'NARA_Risk_Level', 'Size_GB'],
                    ['format1', 'v1', 'High Risk', 1.0],
                    ['format2', 'v2', 'Moderate Risk', 2.0],
                    ['format3', 'v3', 'Low Risk', 3.0],
                    ['format4', 'v4', 'No Match', 4.0]]
        self.assertEqual(result, expected, "Problem with test for unique")


if __name__ == '__main__':
    unittest.main()
