"""
Tests for the function match_nara_risk(), which adds NARA risk information to a dataframe of format identifications.

To simplify the tests, the input dataframe (new_risk_df) only has format columns needed for matching and
tests use an abbreviated NARA Preservation Action Plan CSV (only the columns needed and far fewer formats).
This test input must be updated to keep in sync with changes to new_risk_df or the NARA CSV.
"""
import numpy as np
import os
import pandas as pd
import unittest
from risk_update import match_nara_risk, read_nara_csv


def make_df(df_rows):
    """Make and return a dataframe with consistent column names."""
    column_names = ['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID']
    df = pd.DataFrame(df_rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Reads NARA CSV into a dataframe and renames the columns. Used by every test."""
        nara_csv = os.path.join('test_data', 'NARA_PreservationActionPlan.csv')
        self.nara_risk_df = read_nara_csv(nara_csv)

    def test_technique_1(self):
        """Test for format and NARA have PUID and match on PUID and version extracted from NARA name."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.pdf', 'PDF', 1.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/14'],
                ['path/file.rtf', 'Rich Text Format', 1.5, 'https://www.nationalarchives.gov.uk/pronom/fmt/50'],
                ['path/file.rtf', 'Rich Text Format', 1.6, 'https://www.nationalarchives.gov.uk/pronom/fmt/50']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.pdf', 'PDF', 1.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/14',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain',
                     'PRONOM and Version'],
                    ['path/file.rtf', 'Rich Text Format', 1.5, 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version'],
                    ['path/file.rtf', 'Rich Text Format', 1.6, 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.6', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 1")

    def test_technique_2_case(self):
        """Test for format and NARA have PUID and match on PUID and name but not version extracted from NARA name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.pdf', 'Portable Document Format/Archiving (PDF/A-1a) accessible', '1A', 'https://www.nationalarchives.gov.uk/pronom/fmt/95'],
                ['path/file.rtf', 'Rich Text Format 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.pdf', 'Portable Document Format/Archiving (PDF/A-1a) accessible', '1A',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'PRONOM and Name'],
                    ['path/file.rtf', 'Rich Text Format 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Name']]
        self.assertEqual(result, expected, "Problem with test for technique 2, case same")

    def test_technique_2(self):
        """Test for format and NARA have PUID and match on PUID and name but not version extracted from NARA name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.pdf', 'portable document format/archiving (PDF/A-1a) accessible', '1A', 'https://www.nationalarchives.gov.uk/pronom/fmt/95'],
                ['path/file.rtf', 'RICH TEXT FORMAT 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.pdf', 'portable document format/archiving (PDF/A-1a) accessible', '1A',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95',
                     'Portable Document Format/Archiving (PDF/A-1a) accessible', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/95', 'Low Risk', 'Retain', 'PRONOM and Name'],
                    ['path/file.rtf', 'RICH TEXT FORMAT 1.5', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Rich Text Format 1.5', 'rtf', 'https://www.nationalarchives.gov.uk/pronom/fmt/50',
                     'Moderate Risk', 'Transform to PDF', 'PRONOM and Name']]
        self.assertEqual(result, expected, "Problem with test for technique 2, case different")

    def test_technique_3(self):
        """Test for format and NARA have PUID and match on PUID but not version or name."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.html', 'HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96'],
                ['path/file.pdf', 'PDF 1.0', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.html', 'HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Hypertext Markup Language 5.2', 'htm|html', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Low Risk', 'Retain', 'PRONOM'],
                    ['path/file.html', 'HTML', 'v5.1', 'https://www.nationalarchives.gov.uk/pronom/fmt/96',
                     'Hypertext Markup Language unspecified version', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain', 'PRONOM'],
                    ['path/file.pdf', 'PDF 1.0', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/14',
                     'Portable Document Format (PDF) version 1.0', 'pdf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/14', 'Moderate Risk', 'Retain', 'PRONOM']]
        self.assertEqual(result, expected, "Problem with test for technique 3")

    def test_technique_4_puid_case(self):
        """Test for format has PUID and NARA does not have a PUID and match on name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.pdf', 'Portable Document Format (PDF) Portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.wpt', 'WordPerfect Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.pdf', 'Portable Document Format (PDF) Portfolio', 2.0,
                     'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', np.nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'Format Name'],
                    ['path/file.wpt', 'WordPerfect Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', np.nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, format PUID, case same")

    def test_technique_4_puid(self):
        """Test for format has PUID and NARA does not have a PUID and match on name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.pdf', 'portable document format (pdf) portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.wpt', 'WORDPERFECT TEMPLATE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.pdf', 'portable document format (pdf) portfolio', 2.0,
                     'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', np.nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'Format Name'],
                    ['path/file.wpt', 'WORDPERFECT TEMPLATE', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', np.nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, format PUID, case different")

    def test_technique_4_case(self):
        """Test for format has no PUID (NARA may) and match on name.
        The case of format and NARA names is the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.rtf', 'Rich Text Format', 1.5, 'NO VALUE'],
                ['path/file.wpt', 'WordPerfect Template', 'NO VALUE', 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.rtf', 'Rich Text Format', 1.5, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'Format Name'],
                    ['path/file.wpt', 'WordPerfect Template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', np.nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, no format PUID, case same")

    def test_technique_4(self):
        """Test for format has no PUID (NARA may) and match on name.
        The case of format and NARA names is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.rtf', 'RICH TEXT FORMAT', 1.5, 'NO VALUE'],
                ['path/file.wpt', 'wordperfect template', 'NO VALUE', 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.rtf', 'RICH TEXT FORMAT', 1.5, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'Format Name'],
                    ['path/file.wpt', 'wordperfect template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', np.nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'Format Name']]
        self.assertEqual(result, expected, "Problem with test for technique 4, no format PUID, case different")

    def test_technique_5_puid_case(self):
        """Test for format has PUID and NARA does not have a PUID. Match on extension and version.
        The case of format and NARA extensions is the same."""
        # Creates a dataframe with the format identifications for function input.
        rows = [['path/file.ntf', 'Imagery Format', 1.1, 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.pdf', 'PDF Portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.ntf', 'Imagery Format', 1.1, 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format 1.1', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension and Version'],
                    ['path/file.pdf', 'PDF Portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', np.nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'File Extension and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 5, format PUID, case same")

    def test_technique_5_puid(self):
        """Test for format has PUID and NARA does not have a PUID. Match on extension and version.
        The case of format and NARA extensions is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.NITF', 'Imagery Format', 1.1, 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.pDf', 'PDF Portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.NITF', 'Imagery Format', 1.1, 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format 1.1', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension and Version'],
                    ['path/file.pDf', 'PDF Portfolio', 2.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'Portable Document Format (PDF) Portfolio 2.0', 'pdf', np.nan, 'Moderate Risk',
                     'Retain but possibly extract files from the container', 'File Extension and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 5, format PUID, case different")

    def test_technique_5_case(self):
        """Test for format has no PUID (NARA may) and match on extension and version.
        The case of format and NARA extensions is the same."""
        # Creates a dataframe with the format identifications for function input.
        rows = [['path/file.html', 'HTML', 5.2, 'NO VALUE'],
                ['path/file.pdf', 'PDF Portfolio', 2.0, 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.html', 'HTML', 5.2, 'NO VALUE', 'Hypertext Markup Language 5.2', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain',
                     'File Extension and Version'],
                    ['path/file.pdf', 'PDF Portfolio', 2.0, 'NO VALUE', 'Portable Document Format (PDF) Portfolio 2.0',
                     'pdf', np.nan, 'Moderate Risk', 'Retain but possibly extract files from the container',
                     'File Extension and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 5, no format PUID, case same")

    def test_technique_5(self):
        """Test for format has no PUID (NARA may) and match on extension and version.
        The case of format and NARA extensions is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.HTM', 'HTML', 5.2, 'NO VALUE'],
                ['path/file.Pdf', 'PDF Portfolio', 2.0, 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.HTM', 'HTML', 5.2, 'NO VALUE', 'Hypertext Markup Language 5.2', 'htm|html',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/96', 'Low Risk', 'Retain',
                     'File Extension and Version'],
                    ['path/file.Pdf', 'PDF Portfolio', 2.0, 'NO VALUE', 'Portable Document Format (PDF) Portfolio 2.0',
                     'pdf', np.nan, 'Moderate Risk', 'Retain but possibly extract files from the container',
                     'File Extension and Version']]
        self.assertEqual(result, expected, "Problem with test for technique 5, no format PUID, case different")

    def test_technique_6_puid_case(self):
        """Test for format has PUID and NARA does not have a PUID. Match on extension.
        The case of format and NARA extensions is the same."""
        # Creates a dataframe with the format identifications for function input.
        rows = [['path/file.ntf', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.wpt', 'WP Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.ntf', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format 1.1', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension'],
                    ['path/file.ntf', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format unspecified version', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension'],
                    ['path/file.wpt', 'WP Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', np.nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'File Extension']]
        self.assertEqual(result, expected, "Problem with test for technique 6, format PUID, case same")

    def test_technique_6_puid(self):
        """Test for format has PUID and NARA does not have a PUID. Match on extension.
        The case of format and NARA extensions is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.NITF', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0'],
                ['path/file.WPT', 'WP Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.NITF', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format 1.1', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension'],
                    ['path/file.NITF', 'Imagery Format', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/0',
                     'National Imagery Transmission Format unspecified version', 'ntf|nitf', np.nan, 'Low Risk',
                     'Transform to a TBD format', 'File Extension'],
                    ['path/file.WPT', 'WP Template', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/00',
                     'WordPerfect Template', 'wpt', np.nan, 'Moderate Risk', 'Transform to PDF if possible',
                     'File Extension']]
        self.assertEqual(result, expected, "Problem with test for technique 6, format PUID, case different")

    def test_technique_6_case(self):
        """Test for format has no PUID (NARA may) and match on extension.
        The case of format and NARA extensions is the same."""
        # Creates a dataframe with the format identifications for function input.
        rows = [['path/file.rtf', 'Text', 1.4, 'NO VALUE'],
                ['path/file.wpt', 'WP Template', 'NO VALUE', 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.rtf', 'Text', 1.4, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'File Extension'],
                    ['path/file.rtf', 'Text', 1.4, 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'File Extension'],
                    ['path/file.wpt', 'WP Template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', np.nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'File Extension']]
        self.assertEqual(result, expected, "Problem with test for technique 6, no format PUID, case same")

    def test_technique_6(self):
        """Test for format has no PUID (NARA may) and match on extension.
        The case of format and NARA extensions is not the same."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.RTF', 'Text', 1.4, 'NO VALUE'],
                ['path/file.WPT', 'WP Template', 'NO VALUE', 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.RTF', 'Text', 1.4, 'NO VALUE', 'Rich Text Format 1.5', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'File Extension'],
                    ['path/file.RTF', 'Text', 1.4, 'NO VALUE', 'Rich Text Format 1.6', 'rtf',
                     'https://www.nationalarchives.gov.uk/pronom/fmt/50', 'Moderate Risk', 'Transform to PDF',
                     'File Extension'],
                    ['path/file.WPT', 'WP Template', 'NO VALUE', 'NO VALUE', 'WordPerfect Template', 'wpt', np.nan,
                     'Moderate Risk', 'Transform to PDF if possible', 'File Extension']]
        self.assertEqual(result, expected, "Problem with test for technique 6, no format PUID, case different")

    def test_no_match_puid(self):
        """Test for format has PUID and does not match NARA."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.xlsx', 'Excel', 3.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/56'],
                ['path/file.one', 'OneNote', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/637']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.xlsx', 'Excel', 3.0, 'https://www.nationalarchives.gov.uk/pronom/fmt/56', 'No Match', np.nan, np.nan,
                     'No Match', np.nan, 'No NARA Match'],
                    ['path/file.one', 'OneNote', 'NO VALUE', 'https://www.nationalarchives.gov.uk/pronom/fmt/637', 'No Match',
                     np.nan, np.nan, 'No Match', np.nan, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for no match, format PUID")

    def test_no_match(self):
        """Test for format has no PUID and does not match NARA."""
        # Creates test input: a dataframe with the format identifications and a dataframe with the NARA data.
        rows = [['path/file.xlsx', 'Excel', 3.0, 'NO VALUE'],
                ['path/file.one', 'OneNote', 'NO VALUE', 'NO VALUE']]
        new_risk_df = make_df(rows)

        # Runs the function being tested and converts the resulting dataframe to a list for easier comparison.
        new_risk_df = match_nara_risk(new_risk_df, self.nara_risk_df)
        result = [new_risk_df.columns.tolist()] + new_risk_df.values.tolist()

        # Tests the contents of new_risk_df is correct.
        expected = [['FITS_File_Path', 'FITS_Format_Name', 'FITS_Format_Version', 'FITS_PUID', 'NARA_Format_Name',
                     'NARA_File_Extensions', 'NARA_PRONOM_URL', 'NARA_Risk_Level', 'NARA_Proposed_Preservation_Plan',
                     'NARA_Match_Type'],
                    ['path/file.xlsx', 'Excel', 3.0, 'NO VALUE', 'No Match', np.nan, np.nan,
                     'No Match', np.nan, 'No NARA Match'],
                    ['path/file.one', 'OneNote', 'NO VALUE', 'NO VALUE', 'No Match', np.nan, np.nan,
                     'No Match', np.nan, 'No NARA Match']]
        self.assertEqual(result, expected, "Problem with test for no match, format no PUID")


if __name__ == '__main__':
    unittest.main()
