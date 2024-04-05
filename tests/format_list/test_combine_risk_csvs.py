"""
Test for the function combine_risk_csvs(), which finds all risk csvs in a directory and combines them into one df.
"""
import unittest
from format_list import combine_risk_csvs
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_function(self):
        df_all = combine_risk_csvs(join(getcwd(), 'test_data'))
        df_all = df_all.fillna('nan')
        result = [df_all.columns.tolist()] + df_all.values.tolist()
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB', 
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message', 
                     'NARA_Format Name', 'NARA_File Extension(s)', 'NARA_PRONOM URL', 'NARA_Risk Level', 
                     'NARA_Proposed Preservation Plan', 'NARA_Match_Type', 'Technical Appraisal_Format', 
                     'Technical Appraisal_Trash', 'Other Risk Indicator', 'Technical_Appraisal', 'Other_Risk'],
                    ['C:\\coll1\\acc1a\\Folder\\file1.pdf', 'Portable Document Format', 1.4, 'pronom/fmt/18',
                     'Droid version 6.4; Jhove version 1.20.1', False, '1/9/2018', 410000.486,
                     'c4cb5a0dbad80a7501a445f7857c165d', 'Developer Express Inc. DXperience (tm) v17.1.3/',
                     False, True, '23 severity=error offset=41335', 'Portable Document Format (PDF) version 1.4',
                     'pdf', 'pronom/fmt/18', 'Moderate Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll1\\acc1a\\Folder\\file2.pdf', 'JPEG File Interchange Format', 1.01, 'pronom/fmt/43',
                     'Droid version 6.4; Jhove version 1.20.1', False, '3/11/2017', 220000.139,
                     '2206c72d65eeb5b834b8de1a3474e943', 'nan', True, True, 'nan', 'JPEG File Interchange Format 1.01',
                     'jpg|jpeg', 'pronom/fmt/43', 'Low Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll1\\acc1a\\Folder\\file3.pdf', 'JPEG File Interchange Format', 1.02, 'pronom/fmt/44',
                     'Droid version 6.4; Jhove version 1.20.1', False, '1/4/2017', 183000.783,
                     'a34f624cde40284465ed6eaccd52162d', 'nan', True, True, 'nan', 'JPEG File Interchange Format 1.02',
                     'jpg|jpeg', 'pronom/fmt/44', 'Low Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll1\\acc1a\\Folder\\file4.pdf', 'Portable Document Format', 1.4, 'pronom/fmt/19',
                     'Droid version 6.4; Jhove version 1.20.1', False, '2/9/2017', 94000.626,
                     'b5c39501aefa8efdc0fef28ed58ebc84', 'ABBYY FineReader for ScanSnap 5.0', True, True, 'nan',
                     'Portable Document Format (PDF) version 1.5', 'pdf', 'pronom/fmt/18', 'Moderate Risk', 'Retain',
                     'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll1\\acc1b\\Scan 3.jpeg', 'JPEG File Interchange Format', 1.02,'pronom/fmt/44',
                     'Droid version 6.4; Jhove version 1.20.1', False, '6/5/2023', 110.597,
                     '511fc94a8a86ebfc367b7e028567eb78', 'nan', True, True, 'nan', 'JPEG File Interchange Format 1.02',
                     'jpg|jpeg', 'pronom/fmt/44', 'Low Risk', 'Retain', 'PRONOM and Version', 'nan', 'nan', 'nan',
                     'Not for TA', 'Not for Other'],
                    ['C:\\coll1\\acc1b\\\\Scan 4.jpeg', 'JPEG File Interchange Format', 1.02, 'pronom/fmt/44',
                     'Droid version 6.4; Jhove version 1.20.1', False, '6/5/2023', 95.086,
                     '0c4ba891fbfeee2141fa5ccbf54dd644', 'nan', True, True, 'nan', 'JPEG File Interchange Format 1.02',
                     'jpg|jpeg', 'pronom/fmt/44', 'Low Risk', 'Retain', 'PRONOM and Version', 'nan', 'nan', 'nan',
                     'Not for TA', 'Not for Other'],
                    ['C:\\coll2\\acc2a\\Documents\\7304.jpg', 'JPEG File Interchange Format', '1.01', 'pronom/fmt/43',
                     'Droid version 6.4; Jhove version 1.20.1', False, '4/28/2022', 82638000.0,
                     '61cc2c8de88c59d2f63ba6cb37994ea5', 'nan', True, True, 'nan', 'JPEG File Interchange Format 1.01',
                     'jpg|jpeg', 'pronom/fmt/43', 'Low Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll2\\acc2a\\Documents\\1.png', 'Portable Network Graphics', '1', 'pronom/fmt/11',
                     'Droid version 6.4', False, '4/12/2021', 257638000.0, 'd73dd4bd8073d4639eebfca0db30feab',
                     'nan', 'nan', 'nan', 'nan', 'Portable Network Graphics 1.0', 'png', 'pronom/fmt/11',
                     'Moderate Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll2\\acc2a\\Documents\\2.png', 'Portable Network Graphics', '1', 'pronom/fmt/11',
                     'Droid version 6.4', False, '4/12/2021', 205688000.0, 'e3e67ae007d38d7d3a48cdab087bae31', 'nan',
                     'nan', 'nan', 'nan', 'Portable Network Graphics 1.0', 'png', 'pronom/fmt/11', 'High Risk',
                     'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll2\\acc2a\\Documents\\201.txt', 'Plain text', 'nan', 'pronom/x-fmt/111',
                     'Droid version 6.4', False, '11/4/2013', 5113000.0, '1a4c1cbf30ebbe6bbd74ad346d8c3d69', 'nan',
                     True, True, 'nan', 'Plain Text', 'Plain_Text|txt|text|asc|rte', 'pronom/x-fmt/111',
                     'Moderate Risk', 'Retain', 'PRONOM', False, False, False, 'nan', 'nan'],
                    ['C:\\coll2\\acc2a\\Documents\\201.pdf', 'PDF/A', '1b', 'nan', 'Jhove version 1.20.1', False,
                     '11/4/2013', 45837000.0, 'fb7f8a57a7a341ff67b1f75abae357af', 'Corel PDF Engine', True, True,
                     'nan', 'Portable Document Format/Archiving (PDF/A-2u) unicode', 'pdf', 'pronom/fmt/478',
                     'Low Risk', 'Retain', 'File Extension', False, False, False, 'nan', 'nan'],
                    ['C:\\coll2\\acc2a\\Documents\\201.pdf', 'PDF/A', '1b', 'nan', 'Jhove version 1.20.1', False,
                     '11/4/2013', 45837000.0, 'fb7f8a57a7a341ff67b1f75abae357af', 'Corel PDF Engine', True, True,
                     'nan', 'Portable Document Format/Archiving (PDF/A-3a) accessible', 'pdf', 'pronom/fmt/479',
                     'Low Risk', 'Retain', 'File Extension', False, False, False, 'nan', 'nan']]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
