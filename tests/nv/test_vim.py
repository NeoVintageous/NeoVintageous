from NeoVintageous.tests import unittest

from NeoVintageous.nv.vim import mode_to_name


class TestVim(unittest.TestCase):

    def test_mode_to_name(self):
        self.assertEqual(mode_to_name(unittest.INSERT), 'INSERT')
        self.assertEqual(mode_to_name(unittest.INTERNAL_NORMAL), '')
        self.assertEqual(mode_to_name(unittest.NORMAL), '')
        self.assertEqual(mode_to_name(unittest.OPERATOR_PENDING), '')
        self.assertEqual(mode_to_name(unittest.VISUAL), 'VISUAL')
        self.assertEqual(mode_to_name(unittest.VISUAL_BLOCK), 'VISUAL BLOCK')
        self.assertEqual(mode_to_name(unittest.VISUAL_LINE), 'VISUAL LINE')
        self.assertEqual(mode_to_name(unittest.UNKNOWN), 'UNKNOWN')
        self.assertEqual(mode_to_name(unittest.REPLACE), 'REPLACE')
        self.assertEqual(mode_to_name(unittest.SELECT), 'SELECT')
        self.assertEqual(mode_to_name(unittest.INSERT), 'INSERT')
        self.assertEqual(mode_to_name('foobar'), 'REALLY UNKNOWN')
