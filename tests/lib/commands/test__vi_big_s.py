import unittest

from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_big_s_InModeInternalNormal(ViewTestCase):
    def test_deletes_whole_line(self):
        self.write(''.join(('foo bar\nfoo bar\nfoo bar\n',)))
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 7)))

        self.view.run_command('_vi_big_s_action', {'mode': modes.INTERNAL_NORMAL})
        self.assertEqual(self.view.substr(self.R(0, self.view.size())), 'foo bar\n\nfoo bar\n')

#     def testReindents(self):
#         content = """\tfoo bar
# foo bar
# foo bar
# """
#         self.write(content)
#         self.clear_sel()
#         self.add_sel(self.R((1, 0), (1, 7)))

#         self.view.run_command('_vi_big_s_action', {'mode': modes.INTERNAL_NORMAL})
#         expected = """\t foo bar
# \tfoo bar
# """
#         self.assertEqual(self.view.substr(self.R(0, self.view.size())), '\tfoo bar\n\t\nfoo bar\n')

    @unittest.skip("Implement")
    def test_can_delete_with_count(self):
        self.assertTrue(False)
