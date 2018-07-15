
'''
===============================
Unit tests for module renderers
===============================

Unit tests for renderers
'''

import unittest
from tkipy.renderers import html_table

class Test_html_table(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(str(html_table([[1,2], [3,4]], header_row=['col_1', 'col_2'])), '<table><tr><th>col_1</th><th>col_2</th></tr><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></table>')

if __name__ == '__main__':
    unittest.main()
