"""
Tests for the function combine_collection_data(), which combines data from multiple accessions of the same collection.
If there is only one accession, the collection information is the same as the accession's.
"""
import unittest
from collection_summary import combine_collection_data
from pandas import DataFrame


class MyTestCase(unittest.TestCase):

    def test_multiple(self):
        """Test for when each collection has multiple accessions"""
        # Makes test input and runs the function.
        accession_df = DataFrame([['coll1', 'backlog', 30, 591, '2021-11-15', 90, 0, 365, 136],
                                  ['coll1', 'backlog', 6.4, 102, '2021-12-01', 0, 0, 40, 62],
                                  ['coll1', 'backlog', 0.2, 3, '2022-01-30', 0, 3, 0, 0],
                                  ['coll2', 'closed', 90.0, 67, '2023-02-01', 30, 0, 0, 37],
                                  ['coll2', 'closed', 33.3, 15, '2023-07-01', 0, 0, 0, 15]],
                                 columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk',
                                          'High_Risk', 'Moderate_Risk', 'Low_Risk'])
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        collection_list = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected_list = [['Collection', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                          'Moderate_Risk_%', 'Low_Risk_%'],
                         ['coll1', 'backlog', 36.6, 696, 12.9, 0.4, 58.2, 28.4],
                         ['coll2', 'closed', 123.3, 82, 36.6, 0.0, 0.0, 63.4]]
        self.assertEqual(collection_list, expected_list, "Problem with test for one accession")

    def test_one(self):
        """Test for when each collection has one accession"""
        # Makes test input and runs the function.
        accession_df = DataFrame([['coll1', 'backlog', 23.5, 51, '2023-05-12', 2, 0, 17, 32],
                                  ['coll2', 'backlog', 123.2, 250, '2024-02-01', 100, 54, 33, 63]],
                                 columns=['Collection', 'Status', 'GB', 'Files', 'Date', 'No_Match_Risk',
                                          'High_Risk', 'Moderate_Risk', 'Low_Risk'])
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        collection_list = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected_list = [['Collection', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                          'Moderate_Risk_%', 'Low_Risk_%'],
                         ['coll1', 'backlog', 23.5, 51, 3.9, 0.0, 33.3, 62.7],
                         ['coll2', 'backlog', 123.2, 250, 40.0, 21.6, 13.2, 25.2]]
        self.assertEqual(collection_list, expected_list, "Problem with test for one accession")


if __name__ == '__main__':
    unittest.main()
