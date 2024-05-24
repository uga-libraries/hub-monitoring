"""
Tests for the function combine_collection_data(), which combines data from multiple accessions of the same collection.
If there is only one accession, the collection information is the same as the accession's.
"""
import unittest
from collection_summary import combine_collection_data
from pandas import DataFrame


def make_df(df_rows):
    """Make and return a dataframe with consistent column names."""
    column_names = ['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk',
                    'High_Risk', 'Moderate_Risk', 'Low_Risk', 'Notes']
    df = DataFrame(df_rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_multiple(self):
        """Test for when each collection has multiple accessions"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlog', '2021', 30.01, 607, 90, 0, 17, 500, ''],
                ['acc1b', 'coll1', 'backlog', '2021', 6.35, 80, 0, 0, 40, 40, ''],
                ['acc1c', 'coll1', 'backlog', '2022', 0.25, 9, 0, 9, 0, 0, ''],
                ['acc2a', 'coll2', 'closed', '2023', 90.12, 67, 30, 0, 0, 37, ''],
                ['acc2b', 'coll2', 'closed', '2023', 33.10, 15, 0, 0, 0, 15, '']]
        acc_df = make_df(rows)
        collection_df = combine_collection_data(acc_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['coll1', '2021-2022', 'backlog', 36.61, 696, 90, 9, 57, 540, ''],
                    ['coll2', '2023', 'closed', 123.22, 82, 30, 0, 0, 52, '']]
        self.assertEqual(result, expected, "Problem with test for multiple accessions")

    def test_no_csv(self):
        """Test for when collections (one or multiple accessions) with no risk csvs"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlog', '2021', 30.01, 607, 0, 0, 0, 0, 'Accession 1a has no risk csv. '],
                ['acc1b', 'coll1', 'backlog', '2022', 6.35, 80, 0, 0, 0, 0, 'Accession 1b has no risk csv. '],
                ['acc2a', 'coll2', 'backlog', '2022', 0.25, 9, 0, 0, 0, 0, 'Accession 2a has no risk csv. ']]
        acc_df = make_df(rows)
        collection_df = combine_collection_data(acc_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['coll1', '2021-2022', 'backlog', 36.36, 687, 0, 0, 0, 0,
                     'Accession 1a has no risk csv. Accession 1b has no risk csv. '],
                    ['coll2', '2022', 'backlog', 0.25, 9, 0, 0, 0, 0, 'Accession 2a has no risk csv. ']]
        self.assertEqual(result, expected, "Problem with test for no accessions have a risk csv")

    def test_no_csv_mix(self):
        """Test for when a collection has multiple accessions and one does not have a risk csv"""
        # Makes test input and runs the function.
        rows = [['acc2a', 'coll2', 'closed', '2023', 90.12, 67, 30, 0, 0, 37, ''],
                ['acc2b', 'coll2', 'closed', '2023', 33.10, 33, 0, 0, 0, 0, 'Accession 2023-01-er has no risk csv. ']]
        acc_df = make_df(rows)
        collection_df = combine_collection_data(acc_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['coll2', '2023', 'closed', 123.22, 100, 30, 0, 0, 37, 'Accession 2023-01-er has no risk csv. ']]
        self.assertEqual(result, expected, "Problem with test for an accession doesn't have a risk csv")

    def test_one(self):
        """Test for when each collection has one accession with a risk csv"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlog', '2023', 23.52, 51, 2, 0, 17, 32, ''],
                ['acc2a', 'coll2', 'backlog', '2024', 123.20, 250, 100, 54, 33, 63, '']]
        acc_df = make_df(rows)
        collection_df = combine_collection_data(acc_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes'],
                    ['coll1', '2023', 'backlog', 23.52, 51, 2, 0, 17, 32, ''],
                    ['coll2', '2024', 'backlog', 123.2, 250, 100, 54, 33, 63, '']]
        self.assertEqual(result, expected, "Problem with test for one accession")


if __name__ == '__main__':
    unittest.main()
