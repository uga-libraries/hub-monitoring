"""
Tests for the function combine_collection_date(), which gets the date or date range for a collection.

For simplicity, the acc_df used for testing only has the columns used by this function, Collection and Date.
"""
import unittest
from collection_summary import combine_collection_dates
from pandas import DataFrame


def make_df(df_rows):
    """Make and return a dataframe with consistent column headers."""
    column_names = ['Collection', 'Date']
    df = DataFrame(df_rows, columns=column_names)
    return df


class MyTestCase(unittest.TestCase):

    def test_multiple_diff_years(self):
        """Test for accessions that have multiple accession dates, all different years"""
        # Makes test input and runs the function.
        rows = [['coll_1', '2000'], ['coll_1', '2012'], ['coll_2', '1999'], ['coll_2', '1997'], ['coll_2', '1998']]
        acc_df = make_df(rows)
        date_df = combine_collection_dates(acc_df)

        # Verifies the dataframe has the expected contents, converting it to a list first for easier comparison.
        result = [date_df.columns.tolist()] + date_df.values.tolist()
        expected = [['Collection', 'Date'], ['coll_1', '2000-2012'], ['coll_2', '1997-1999']]
        self.assertEqual(expected, result, "Problem with test for multiple different years")

    def test_multiple_same_years(self):
        """Test for accessions that have multiple accession dates, all the same year"""
        # Makes test input and runs the function.
        rows = [['coll_1', '2001'], ['coll_1', '2001'], ['coll_2', '2013'], ['coll_2', '2013'], ['coll_2', '2013']]
        acc_df = make_df(rows)
        date_df = combine_collection_dates(acc_df)

        # Verifies the dataframe has the expected contents, converting it to a list first for easier comparison.
        result = [date_df.columns.tolist()] + date_df.values.tolist()
        expected = [['Collection', 'Date'], ['coll_1', '2001'], ['coll_2', '2013']]
        self.assertEqual(expected, result, "Problem with test for multiple of the same year")

    def test_one_year(self):
        """Test for accessions that have one accession date, which is a year"""
        # Makes test input and runs the function.
        rows = [['coll_1', '2023'], ['coll_2', '2014']]
        acc_df = make_df(rows)
        date_df = combine_collection_dates(acc_df)

        # Verifies the dataframe has the expected contents, converting it to a list first for easier comparison.
        result = [date_df.columns.tolist()] + date_df.values.tolist()
        expected = [['Collection', 'Date'], ['coll_1', '2023'], ['coll_2', '2014']]
        self.assertEqual(expected, result, "Problem with test for one year")


if __name__ == '__main__':
    unittest.main()
