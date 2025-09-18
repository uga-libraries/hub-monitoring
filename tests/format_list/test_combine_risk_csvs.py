"""
Test for the function combine_risk_csvs(), which finds all risk csvs in a directory and combines them into one df.
"""
import unittest
from format_list import combine_risk_csvs
from test_df_cleanup import df_to_list
from os import getcwd
from os.path import join


class MyTestCase(unittest.TestCase):

    def test_multiple_risks(self):
        """
        Test for an input_directory with multiple risk csvs per accession,
        with an input_directory as if the script is running on a born digital folder
        """
        input_directory = join(getcwd(), 'combine_test_data', 'multiple-risks')
        df_all = combine_risk_csvs(input_directory)

        result = df_to_list(df_all)
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format Name', 'NARA_File Extension(s)', 'NARA_PRONOM URL', 'NARA_Risk Level',
                     'NARA_Proposed Preservation Plan', 'NARA_Match_Type', 'Technical_Appraisal', 'Other_Risk'],
                    ['Z:\\multiple-risks\\backlogged\\coll_1\\acc_1a_er\\001_na.jpg', 'JPEG EXIF', 1.01, 'nan',
                     'Jhove version 1.20', False, '2020-02-06', 294.094, 'bad8d3d26720ecd5dd45cd3b8f71fd45', 'nan',
                     True, True, 'nan', 'JPEG File Interchange Format 1.01', 'jpg|jpeg',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Low Risk', 'Retain',
                     'File Extension and Version', 'Not for TA', 'Not for Other'],
                    ['Z:\\multiple-risks\\backlogged\\coll_1\\acc_1a_er\\Awards.doc',
                     'Microsoft Word Binary File Format', 'nan', 'nan', 'Exiftool version 11.54', False, '2011-06-27',
                     76.8, '5760bc9c5f0a3ff3ec0dd9a71188ad9a', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Interleaf Document', 'ildoc|doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/329',
                     'High Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\multiple-risks\\closed\\coll_a\\acc_a1_er\\001_na.jpg', 'JPEG EXIF', 1.01, 'nan',
                     'Jhove version 1.20', False, '2020-02-06', 294.094, 'bad8d3d26720ecd5dd45cd3b8f71fd45',
                     'nan', True, True, 'nan', 'JPEG File Interchange Format 1.01', 'jpg|jpeg',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Low Risk', 'Retain',
                     'File Extension and Version', 'Not for TA', 'Not for Other'],
                    ['Z:\\multiple-risks\\closed\\coll_a\\acc_a1_er\\Awards.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2011-06-27', 76.8,
                     '5760bc9c5f0a3ff3ec0dd9a71188ad9a', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Interleaf Document', 'ildoc|doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/329',
                     'High Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other']]

        self.assertEqual(expected, result, "Problem with test for multiple risk csvs per accession")

    def test_one_risk(self):
        """
        Test for an input_directory with one risk csv,
        with an input_directory as if the script is running on a single collection folder
        """
        input_directory = join(getcwd(), 'combine_test_data', 'one-risk', 'acc-1-er')
        df_all = combine_risk_csvs(input_directory)

        result = df_to_list(df_all)
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format Name', 'NARA_File Extension(s)', 'NARA_PRONOM URL', 'NARA_Risk Level',
                     'NARA_Proposed Preservation Plan', 'NARA_Match_Type', 'Technical_Appraisal', 'Other_Risk'],
                    ['Z:\\digital\\one-risk\\acc-1-er\\001.jpg', 'JPEG File Interchange Format', 1.01,
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Droid version 6.4; Jhove version 1.20.1',
                     False, '2/5/2020', 345.611, '6f3497dcec851ac5bb0b0d9d240f027f',
                     'Intel(R) JPEG Library, version [2.3.0.0]', True, True, 'nan',
                     'JPEG File Interchange Format 1.01', 'jpg|jpeg',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Low Risk', 'Retain', 'PRONOM and Version',
                     'Not for TA', 'Not for Other'],
                    ['Z:\\digital\\one-risk\\acc-1-er\\002.jpg', 'JPEG EXIF', 1.01, 'nan',
                     'Jhove version 1.20.1; NLNZ Metadata Extractor version 3.6GA', False, '2/6/2020', 234.849,
                     'ff41801994e4fcbe66a98f78af7f870a', 'nan', True, True, 'nan',
                     'JPEG File Interchange Format 1.01', 'jpg|jpeg',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/43', 'Low Risk', 'Retain',
                     'File Extension and Version', 'Not for TA', 'Not for Other'],
                    ['Z:\\digital\\one-risk\\acc-1-er\\info.txt', 'Plain text', 'nan',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Droid version 6.4; Jhove version 1.20.1; file utility version 5.03', False, '4/25/2022',
                     0.139, 'dd9f19da4aa187275f1aac48f308452c', 'nan', True, True, 'nan', 'Plain Text',
                     'Plain_Text|txt|text|asc|rte', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/111',
                     'Low Risk', 'Retain', 'PRONOM', 'Not for TA', 'Not for Other'],
                    ['Z:\\digital\\one-risk\\acc-1-er\\manifest.csv', 'Comma-Separated Values (CSV)', 'nan',
                     'https://www.nationalarchives.gov.uk/pronom/x-fmt/18', 'Droid version 6.4', False, '5/25/2023',
                     11.717, 'b0ccf16637f71feb263f645c17c101fd', 'nan', 'nan', 'nan', 'nan',
                     'Comma Separated Values', 'csv', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/18',
                     'Low Risk', 'Retain', 'PRONOM', 'Not for TA', 'Not for Other']]

        self.assertEqual(expected, result, "Problem with test for one risk csv")

    def test_one_risk_each(self):
        """
        Test for an input_directory with one risk csv per accession,
        with an input directory as if the script is running on a single status folder
        """
        input_directory = join(getcwd(), 'combine_test_data', 'one-risk-each', 'closed')
        df_all = combine_risk_csvs(input_directory)

        result = df_to_list(df_all)
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID',
                     'FITS_Identifying_Tool(s)', 'FITS_Multiple_IDs', 'FITS_Date_Last_Modified', 'FITS_Size_KB',
                     'FITS_MD5', 'FITS_Creating_Application', 'FITS_Valid', 'FITS_Well-Formed', 'FITS_Status_Message',
                     'NARA_Format Name', 'NARA_File Extension(s)', 'NARA_PRONOM URL', 'NARA_Risk Level',
                     'NARA_Proposed Preservation Plan', 'NARA_Match_Type', 'Technical_Appraisal', 'Other_Risk'],
                    ['Z:\\one-risk-each\\closed\\coll_1\\acc-1a-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Interleaf Document', 'ildoc|doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/329',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\one-risk-each\\closed\\coll_1\\acc-1a-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Microsoft Word for Macintosh 5.0', 'doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/65',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\one-risk-each\\closed\\coll_1\\acc-1b-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Interleaf Document', 'ildoc|doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/329',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\one-risk-each\\closed\\coll_1\\acc-1b-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Microsoft Word for Macintosh 5.0', 'doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/65',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\one-risk-each\\closed\\coll_2\\acc-2a-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Interleaf Document', 'ildoc|doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/329',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other'],
                    ['Z:\\one-risk-each\\closed\\coll_2\\acc-2a-er\\River.doc', 'Microsoft Word Binary File Format',
                     'nan', 'nan', 'Exiftool version 11.54', False, '2010-12-30', 290.304,
                     '09198237adf2b5f63349df20160dc765', 'Microsoft Office Word', 'nan', 'nan', 'nan',
                     'Microsoft Word for Macintosh 5.0', 'doc', 'https://www.nationalarchives.gov.uk/pronom/x-fmt/65',
                     'Moderate Risk', 'Transform to PDF', 'File Extension', 'Not for TA', 'Not for Other']]

        self.assertEqual(expected, result, "Problem with test for one risk csv each accession")


if __name__ == '__main__':
    unittest.main()
