"""
Tests for the function check_restart(), which determines if the script is being restarted.
"""
import os
import unittest
from validate_fixity import check_restart


class MyTestCase(unittest.TestCase):

    def test_not_restart(self):
        """Test for when the script is not being restarted (log is not present)"""
        # Makes the variable for function input and runs the function.
        input_directory = os.path.join('test_data', 'check_restart', 'restart_no')
        fixity_validation_log_path = check_restart(input_directory)

        # Verifies fixity_validation_log_path has the correct value.
        self.assertEqual(None, fixity_validation_log_path, "Problem with test for not restart")

    def test_restart(self):
        """Test for when the script is being restarted (log is present)"""
        # Makes the variable for function input and runs the function.
        input_directory = os.path.join('test_data', 'check_restart', 'restart_yes')
        fixity_validation_log_path = check_restart(input_directory)

        # Verifies fixity_validation_log_path has the correct value.
        expected = os.path.join('test_data', 'check_restart', 'restart_yes', 'fixity_validation_log_20241031.csv')
        self.assertEqual(expected, fixity_validation_log_path, "Problem with test for restart")


if __name__ == '__main__':
    unittest.main()
