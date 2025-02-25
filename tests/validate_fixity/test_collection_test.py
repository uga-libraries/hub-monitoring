"""
Tests for the function collection_test(), which determines if a folder is an accession.
"""
import unittest
from validate_fixity import collection_test


class MyTestCase(unittest.TestCase):

    def test_harg_ms(self):
        """Test for when the folder matches a Hargrett manuscript collection pattern"""
        parent_dir = 'ms1234 Jane Doe papers'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Hargrett MS')
      
    def test_harg_ua(self):
        """Test for when the folder matches a Hargrett university archives collection pattern with no dash"""
        parent_dir = 'ua1234 Department records'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Hargrett UA')

    def test_harg_ua_dash(self):
        """Test for when the folder matches a Hargrett university archives collection pattern with a dash"""
        parent_dir = 'ua12-345 Department records'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Hargrett UA with dash')

    def test_not_coll_appraisal(self):
        """Test for when the folder does not match any collection patterns (appraisal folder)"""
        parent_dir = 'Appraisal - copy'
        result = collection_test(parent_dir)
        self.assertEqual(result, False, 'Problem with test for not a collection - appraisal')

    def test_not_coll_risk(self):
        """Test for when the folder does not match any collection patterns (risk remediation folder)"""
        parent_dir = 'V2 AIPs - risk remediation'
        result = collection_test(parent_dir)
        self.assertEqual(result, False, 'Problem with test for not a collection - risk')

    def test_rbrl(self):
        """Test for when the folder matches a Russell collection pattern with no underscore or letters"""
        parent_dir = 'rbrl521'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Russell')
    
    def test_rbrl_letters(self):
        """Test for when the folder matches a Russell collection pattern with letters but no underscore"""
        parent_dir = 'rbrl246abc'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Russell with letters')
    
    def test_rbrl_under(self):
        """Test for when the folder matches a Russell collection pattern with underscores but no letters"""
        parent_dir = 'RBRL_356'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Russell with underscores')
    
    def test_rbrl_under_letters(self):
        """Test for when the folder matches a Russell collection pattern with underscores and letters"""
        parent_dir = 'RBRL_240_AB'
        result = collection_test(parent_dir)
        self.assertEqual(result, True, 'Problem with test for Russell with underscores and letters')


if __name__ == '__main__':
    unittest.main()
