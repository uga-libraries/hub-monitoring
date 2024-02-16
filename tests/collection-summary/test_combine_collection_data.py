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
        accession_df = DataFrame([['coll1', 'backlog', '2021', 30, 591, 90, 0, 365, 136],
                                  ['coll1', 'backlog', '2021', 6.4, 102, 0, 0, 40, 62],
                                  ['coll1', 'backlog', '2022', 0.2, 3, 0, 3, 0, 0],
                                  ['coll2', 'closed', '2023', 90.0, 67, 30, 0, 0, 37],
                                  ['coll2', 'closed', '2023', 33.3, 15, 0, 0, 0, 15]],
                                 columns=['Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk',
                                          'High_Risk', 'Moderate_Risk', 'Low_Risk'])
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        collection_list = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected_list = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                          'Moderate_Risk_%', 'Low_Risk_%'],
                         ['coll1', '2021-2022', 'backlog', 36.6, 696, 12.93, 0.43, 58.19, 28.45],
                         ['coll2', '2023', 'closed', 123.3, 82, 36.59, 0.0, 0.0, 63.41]]
        self.assertEqual(collection_list, expected_list, "Problem with test for one accession")

    def test_one(self):
        """Test for when each collection has one accession"""
        # Makes test input and runs the function.
        accession_df = DataFrame([['coll1', 'backlog', '2023', 23.5, 51, 2, 0, 17, 32],
                                  ['coll2', 'backlog', '2024', 123.2, 250, 100, 54, 33, 63]],
                                 columns=['Collection', 'Status', 'Date', 'GB', 'Files', 'No_Match_Risk',
                                          'High_Risk', 'Moderate_Risk', 'Low_Risk'])
        collection_df = combine_collection_data(accession_df)

        # Converts the resulting dataframe into a list for easier comparison, and compares to the expected result.
        collection_list = [collection_df.columns.tolist()] + collection_df.values.tolist()
        expected_list = [['Collection', 'Date', 'Status', 'GB', 'Files', 'No_Match_Risk_%', 'High_Risk_%',
                          'Moderate_Risk_%', 'Low_Risk_%'],
                         ['coll1', '2023', 'backlog', 23.5, 51, 3.92, 0.0, 33.33, 62.75],
                         ['coll2', '2024', 'backlog', 123.2, 250, 40.0, 21.60, 13.20, 25.20]]
        self.assertEqual(collection_list, expected_list, "Problem with test for one accession")


if __name__ == '__main__':
    unittest.main()
