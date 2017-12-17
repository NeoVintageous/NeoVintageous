from NeoVintageous.tests import unittest

from NeoVintageous.lib.ex.completions import wants_fs_completions
from NeoVintageous.lib.ex.completions import wants_setting_completions


class TestCompletions(unittest.ViewTestCase):

    def test_wants_setting_completions(self):
        self.assertFalse(wants_setting_completions('foobar'))
        self.assertFalse(wants_setting_completions(':set'))
        self.assertTrue(wants_setting_completions(':se '))
        self.assertTrue(wants_setting_completions(':set '))
        self.assertTrue(wants_setting_completions(':set '))
        self.assertTrue(wants_setting_completions(':set name'))
        self.assertTrue(wants_setting_completions(':setl '))
        self.assertTrue(wants_setting_completions(':setlocal '))
        self.assertTrue(wants_setting_completions(':setlocal name'))

    def test_wants_fs_completions(self):
        self.assertFalse(wants_fs_completions('foobar'))
        self.assertFalse(wants_fs_completions(':write'))
        self.assertTrue(wants_fs_completions(':w '))
        self.assertTrue(wants_fs_completions(':write '))
        self.assertTrue(wants_fs_completions(':write path'))
