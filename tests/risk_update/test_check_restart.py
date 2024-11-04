"""
Tests for the function check_restart), which determines if the script is being restarted.
"""
import os
import unittest
from risk_update import check_restart


class MyTestCase(unittest.TestCase):

    def test_not_restart(self):
        """Test for when the script is not being restarted (log is not in input_directory)"""
        # Makes the variable for the function input and runs the function.
        input_directory = os.path.join('test_data', 'check_restart', 'restart_false')
        risk_update_log_path = check_restart(input_directory)

        # Verifies risk_update_log_path has the correct value.
        self.assertEqual(risk_update_log_path, None, "Problem with test for not restart")

    def test_restart(self):
        """Test for when the script is being restarted (log is in input_directory)"""
        # Makes the variable for the function input and runs the function.
        input_directory = os.path.join('test_data', 'check_restart', 'restart_true')
        risk_update_log_path = check_restart(input_directory)

        # Verifies risk_update_log_path has the correct value.
        expected = os.path.join(input_directory, 'risk_update_log_20241101.csv')
        self.assertEqual(risk_update_log_path, expected, "Problem with test for restart")


if __name__ == '__main__':
    unittest.main()
