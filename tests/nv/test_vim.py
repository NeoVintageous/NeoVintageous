from NeoVintageous.tests import unittest

from NeoVintageous.nv.vim import INSERT
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import is_visual_mode
from NeoVintageous.nv.vim import mode_to_name
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import OPERATOR_PENDING
from NeoVintageous.nv.vim import REPLACE
from NeoVintageous.nv.vim import SELECT
from NeoVintageous.nv.vim import UNKNOWN
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_BLOCK
from NeoVintageous.nv.vim import VISUAL_LINE


class TestVim(unittest.TestCase):

    def test_mode_to_name(self):
        self.assertEqual(mode_to_name(INSERT), 'INSERT')
        self.assertEqual(mode_to_name(INTERNAL_NORMAL), '')
        self.assertEqual(mode_to_name(NORMAL), '')
        self.assertEqual(mode_to_name(OPERATOR_PENDING), '')
        self.assertEqual(mode_to_name(VISUAL), 'VISUAL')
        self.assertEqual(mode_to_name(VISUAL_BLOCK), 'VISUAL BLOCK')
        self.assertEqual(mode_to_name(VISUAL_LINE), 'VISUAL LINE')
        self.assertEqual(mode_to_name(UNKNOWN), 'UNKNOWN')
        self.assertEqual(mode_to_name(REPLACE), 'REPLACE')
        self.assertEqual(mode_to_name(SELECT), 'SELECT')
        self.assertEqual(mode_to_name(INSERT), 'INSERT')
        self.assertEqual(mode_to_name('foobar'), '*UNKNOWN')

    def test_is_visual_mode(self):
        self.assertFalse(is_visual_mode(INSERT))
        self.assertFalse(is_visual_mode(INTERNAL_NORMAL))
        self.assertFalse(is_visual_mode(NORMAL))
        self.assertFalse(is_visual_mode(OPERATOR_PENDING))
        self.assertFalse(is_visual_mode(REPLACE))
        self.assertFalse(is_visual_mode(SELECT))
        self.assertFalse(is_visual_mode(UNKNOWN))
        self.assertTrue(is_visual_mode(VISUAL))
        self.assertTrue(is_visual_mode(VISUAL_BLOCK))
        self.assertTrue(is_visual_mode(VISUAL_LINE))
