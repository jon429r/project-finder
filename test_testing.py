import unittest
from unittest.mock import patch
from io import StringIO
import sys

# Assuming your main script is named "project_manager.py"
import main

class TestNewCommand(unittest.TestCase):
    @patch("builtins.input", side_effect=["new -name Project1 -dir /path/to/project1\nY\n", "exit\n"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_new_command(self, mock_stdout, mock_input):
        main.main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("Project name: Project1", output)
        self.assertIn("Working directory: /path/to/project1", output)
        self.assertIn("Adding project to database...", output)

if __name__ == "__main__":
    unittest.main()
