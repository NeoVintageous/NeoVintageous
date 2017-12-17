from NeoVintageous.tests import unittest

from NeoVintageous.lib.modeline import modeline


class TestModeline(unittest.ViewTestCase):

    def test_modeline(self):
        self.settings().set('translate_tab_to_spaces', True)
        self.settings().set('gutter', False)
        self.settings().set('rulers', [])
        self.settings().set('tab_size', 2)

        self.write(
            "# sublime: translate_tab_to_spaces false\n"
            "# sublime: gutter true\n"
            "# sublime: tab_size 4\n"
            "# sublime: rulers [80, 120]\n"
        )

        # pre condition
        self.assertTrue(self.settings().get('translate_tab_to_spaces'))
        self.assertFalse(self.settings().get('gutter'))
        self.assertEqual([], self.settings().get('rulers'))
        self.assertEqual(2, self.settings().get('tab_size'))

        modeline(self.view)

        # post condition
        self.assertFalse(self.settings().get('translate_tab_to_spaces'))
        self.assertTrue(self.settings().get('gutter'))
        self.assertEqual([80, 120], self.settings().get('rulers'))
        self.assertEqual(4, self.settings().get('tab_size'))
