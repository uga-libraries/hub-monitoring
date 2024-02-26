"""
Tests for the function match_nara_risk(), which adds NARA risk information to a dataframe of format identifications.

To simplify the tests, the input dataframe (update_df) only has format columns needed for matching and
tests use an abbreviated NARA Preservation Action Plan CSV (only the columns needed and far fewer formats).
This test input must be updated to keep in sync with changes to update_df or the NARA CSV.
"""
import unittest
from risk_update import match_nara_risk
from numpy import nan
from os import getcwd
from os.path import join
from pandas import DataFrame, read_csv


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Reads NARA CSV into a dataframe and renames the columns. Used by every test."""
        nara_csv = join(getcwd(), '..', 'test_data', 'NARA_PreservationActionPlan.csv')
        self.nara_df = read_csv(nara_csv)
        self.nara_df = self.nara_df.rename(columns={'Format Name': 'NARA_Format_Name',
                                                    'File Extension(s)': 'NARA_File_Extensions',
                                                    'PRONOM URL': 'NARA_PRONOM_URL',
                                                    'NARA Risk Level': 'NARA_Risk_Level',
                                                    'NARA Proposed Preservation Plan': 'NARA_Proposed_Preservation_Plan'})

    def test_technique_1(self):
        """Test for format and NARA have PUID and match on PUID and version extracted from NARA name."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['PDF', 1.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/14'],
                               ['Rich Text Format', 1.5, 'https://www.nationalarchives.gov.uk/pronom/fmt/50'],
                               ['Rich Text Format', 1.6, 'https://www.nationalarchives.gov.uk/pronom/fmt/50']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['PDF', 1.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/14',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain',
                     'PRONOM and Version'],
                    ['Rich Text Format', 1.5, 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version'],
                    ['Rich Text Format', 1.6, 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 1")

    def test_technique_2_case(self):
        """Test for format and NARA have PUID and match on PUID and name but not version extracted from NARA name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['Portable Document Format/Archiving (PDF/A-1a) accessible', '1A',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/95'],
                               ['Rich Text Format 1.5', 'NO VALUE',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/50']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Portable Document Format/Archiving (PDF/A-1a) accessible', '1A',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'PRONOM and Name'],
                    ['Rich Text Format 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Name']]
        self.assertEqual(result, expected, "Problem with test for technique 2, case same")

    def test_technique_2(self):
        """Test for format and NARA have PUID and match on PUID and name but not version extracted from NARA name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['portable document format/archiving (PDF/A-1a) accessible', '1A',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/95'],
                               ['RICH TEXT FORMAT 1.5', 'NO VALUE',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/50']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['portable document format/archiving (PDF/A-1a) accessible', '1A',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'PRONOM and Name'],
                    ['RICH TEXT FORMAT 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Name']]
        self.assertEqual(result, expected, "Problem with test for technique 2, case different")

    def test_technique_3(self):
        """Test for format and NARA have PUID and match on PUID but not version or name."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96'],
                               ['PDF 1.0', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Hypertext Markup Language 5.2', 'htm|html', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['PDF 1.0', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain', 'PRONOM']]
        self.assertEqual(result, expected, "Problem with test for technique 3")

    def test_technique_4_puid_case(self):
        """Test for format has PUID and NARA does not have a PUID and match on name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['Portable Document Format (PDF) Portfolio', 2.0,
                                'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                               ['WordPerfect Template', 'NO VALUE',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/00']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Portable Document Format (PDF) Portfolio', 2.0,
                     'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'Format Name'],
                    ['WordPerfect Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, format PUID, case same")

    def test_technique_4_puid(self):
        """Test for format has PUID and NARA does not have a PUID and match on name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['portable document format (pdf) portfolio', 2.0,
                                'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                               ['WORDPERFECT TEMPLATE', 'NO VALUE',
                                'https://www.nationalarchives.gov.uk/pronom/fmt/00']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['portable document format (pdf) portfolio', 2.0,
                     'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'Format Name'],
                    ['WORDPERFECT TEMPLATE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, format PUID, case different")

    def test_technique_4_case(self):
        """Test for format has no PUID (NARA may) and match on name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['Rich Text Format', 1.5, 'NO VALUE'],
                               ['WordPerfect Template', 'NO VALUE', 'NO VALUE']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Rich Text Format', 1.5, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'Format Name'],
                    ['WordPerfect Template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, no format PUID, case same")

    def test_technique_4(self):
        """Test for format has no PUID (NARA may) and match on name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['RICH TEXT FORMAT', 1.5, 'NO VALUE'],
                               ['wordperfect template', 'NO VALUE', 'NO VALUE']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['RICH TEXT FORMAT', 1.5, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'Format Name'],
                    ['wordperfect template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, no format PUID, case different")

    def test_no_match_puid(self):
        """Test for format has PUID and does not match NARA."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['Excel', 3.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/56'],
                               ['OneNote', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/637']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Excel', 3.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/56', 'No Match', nan, nan,
                     'No Match', nan, 'No NARA Match'],
                    ['OneNote', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/637', 'No Match', nan, nan,
                     'No Match', nan, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for no match, format PUID")

    def test_no_match(self):
        """Test for format has no PUID and does not match NARA."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        update_df = DataFrame([['Excel', 3.0, 'NO VALUE'],
                               ['OneNote', 'NO VALUE', 'NO VALUE']],
                              columns=['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID'])

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        update_df = match_nara_risk(update_df, self.nara_df)
        result = [update_df.columns.tolist()] + update_df.values.tolist()

        # Tests the contents of update_df is correct.
        expected = [['FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name', 'NARA_File_Extensions',
                     'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan', 'NARA_Match_Type'],
                    ['Excel', 3.0, 'NO VALUE', 'No Match', nan, nan,
                     'No Match', nan, 'No NARA Match'],
                    ['OneNote', 'NO VALUE', 'NO VALUE', 'No Match', nan, nan,
                     'No Match', nan, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for no match, format no PUID")


if __name__ == '__main__':
    unittest.main()
