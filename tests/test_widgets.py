
'''
=============================
Unit tests for module widgets
=============================

Unit tests for widgets
'''
import unittest
from IPython.display import display
from unittest.mock import patch, Mock
from tkipy.widgets import explore, source_code_display_toggle_button, notebook_full_width

class Test_explore(unittest.TestCase):
    def test_normal(self):
        with patch('IPython.display.display', Mock(display)) as mock_display:
            to_explore = [1,2,3]
            explore(to_explore)
            mock_display.assert_called_with(to_explore)
            self.assertEqual(mock_display.call_count, 2)

class Test_source_code_display_toggle_button(unittest.TestCase):
    def test_normal(self):
        with patch('IPython.display.display', Mock(display)) as mock_display:
            source_code_display_toggle_button()
            mock_display.assert_called()


class Test_notebook_full_width(unittest.TestCase):
    def test_normal(self):
        with patch('IPython.display.display', Mock(display)) as mock_display:
            notebook_full_width()
            mock_display.assert_called()

if __name__ == '__main__':
    unittest.main()
