"""
Tests for the function files_per_format(), which gets the number of files per format name/version/risk combination.
To simplify the test input, tests have the columns needed for that test.
"""
import unittest
from format_list import files_per_format
from test_df_cleanup import df_to_list
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def test_repeats(self):
        """Test for combining repeating name, version, risk combinations"""
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
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
