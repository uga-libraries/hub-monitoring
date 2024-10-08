"""
Tests for the function combine_collection_data(), which combines data from multiple accessions of the same collection.
If there is only one accession, the collection information is the same as the accession's.

If a column's values are all "None", they are 0 in the expected output for this function after list conversion,
but will be saved to the report as blank.
"""
import unittest
from collection_summary import combine_collection_data
from pandas import DataFrame


def make_df(df_rows):
    """Make and return a dataframe with consistent column names."""
    column_names = ['Accession', 'Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk',
                    'High_Risk', 'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error']
    df = DataFrame(df_rows, columns=column_names, dtype=object)
    return df


class MyTestCase(unittest.TestCase):

    def test_multiple(self):
        """Test for when each collection has multiple accessions with no error messages"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlogged', '2021', 30.01, 607, 90, 0, 17, 500, None, None],
                ['acc1b', 'coll1', 'backlogged', '2021', 6.35, 80, 0, 0, 40, 40, None, None],
                ['acc1c', 'coll1', 'backlogged', '2022', 0.25, 9, 0, 9, 0, 0, None, None],
                ['acc2a', 'coll2', 'closed', '2023', 90.12, 67, 30, 0, 0, 37, None, None],
                ['acc2b', 'coll2', 'closed', '2023', 33.10, 15, 0, 0, 0, 15, None, None]]
        accession_df = make_df(rows)
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['coll1', '2021-2022', 'backlogged', 36.61, 696, 90, 9, 57, 540, 0, 0],
                    ['coll2', '2023', 'closed', 123.22, 82, 30, 0, 0, 52, 0, 0]]
        self.assertEqual(result, expected, "Problem with test for multiple accessions")

    def test_multiple_all_errors(self):
        """Test for when a collection has multiple accessions with both error messages"""
        # Makes test input and runs the function.
        rows = [['acc2a', 'coll2', 'closed', '2023', 0, 0, 0, 0, 0, 0, 'Accession acc2a has no risk csv. ',
                 'Did not calculate size for accession acc2a due to folder organization. '],
                ['acc2b', 'coll2', 'closed', '2023', 0, 0, 0, 0, 0, 0, 'Accession acc2b has no risk csv. ',
                 'Did not calculate size for accession acc2b due to path length. ']]
        accession_df = make_df(rows)
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['coll2', '2023', 'closed', 0, 0, 0, 0, 0, 0,
                     'Accession acc2a has no risk csv. Accession acc2b has no risk csv. ',
                     'Did not calculate size for accession acc2a due to folder organization. '
                     'Did not calculate size for accession acc2b due to path length. ']]
        self.assertEqual(result, expected, "Problem with test for multiple accessions, all errors")

    def test_multiple_some_errors(self):
        """Test for when a collection has multiple accessions, some with and some without error messages"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlogged', '2021', 30.01, 607, 0, 0, 0, 0,
                 'Accession acc1a has no risk csv. ', None],
                ['acc1b', 'coll1', 'backlogged', '2021', 0, 0, 0, 0, 0, 0, 'Accession acc1b has no risk csv. ',
                 'Did not calculate size for accession acc1b due to path length. '],
                ['acc1c', 'coll1', 'backlogged', '2022', 0, 0, 0, 9, 0, 1, None,
                 'Did not calculate size for accession acc1c due to path length. '],
                ['acc2a', 'coll2', 'closed', '2023', 90.12, 67, 30, 0, 0, 37, None, None],
                ['acc2b', 'coll2', 'closed', '2023', 33.10, 15, 0, 0, 0, 0, 'Accession acc2b has no risk csv. ', None]]
        accession_df = make_df(rows)
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['coll1', '2021-2022', 'backlogged', 0, 0, 0, 9, 0, 1,
                     'Accession acc1a has no risk csv. Accession acc1b has no risk csv. ',
                     'Did not calculate size for accession acc1b due to path length. '
                     'Did not calculate size for accession acc1c due to path length. '],
                    ['coll2', '2023', 'closed', 123.22, 82, 30, 0, 0, 37, 'Accession acc2b has no risk csv. ', 0]]
        self.assertEqual(result, expected, "Problem with test for multiple accessions, some errors")

    def test_one(self):
        """Test for when each collection has one accession with no error messages"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlogged', '2023', 23.52, 51, 2, 0, 17, 32, None, None],
                ['acc2a', 'coll2', 'backlogged', '2024', 123.20, 250, 100, 54, 33, 63, None, None]]
        accession_df = make_df(rows)
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['coll1', '2023', 'backlogged', 23.52, 51, 2, 0, 17, 32, 0, 0],
                    ['coll2', '2024', 'backlogged', 123.2, 250, 100, 54, 33, 63, 0, 0]]
        self.assertEqual(result, expected, "Problem with test for one accession")

    def test_one_errors(self):
        """Test for when each collection has one accession with both error messages"""
        # Makes test input and runs the function.
        rows = [['acc1a', 'coll1', 'backlogged', '2021', 0, 0, 0, 0, 0, 0, 'Accession 1a has no risk csv. ', 
                 'Did not calculate size for accession acc1a due to path length. '],
                ['acc2a', 'coll2', 'backlogged', '2022', 0, 0, 0, 0, 0, 0, 'Accession 2a has no risk csv. ', 
                 'Did not calculate size for accession acc1b due to path length. ']]
        accession_df = make_df(rows)
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        result = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk', 'High_Risk',
                     'Moderate_Risk', 'Low_Risk', 'Notes', 'Size_Error'],
                    ['coll1', '2021', 'backlogged', 0, 0, 0, 0, 0, 0, 'Accession 1a has no risk csv. ',
                     'Did not calculate size for accession acc1a due to path length. '],
                    ['coll2', '2022', 'backlogged', 0, 0, 0, 0, 0, 0, 'Accession 2a has no risk csv. ',
                     'Did not calculate size for accession acc1b due to path length. ']]
        self.assertEqual(result, expected, "Problem with test for one accession, all errors")


if __name__ == '__main__':
    unittest.main()
