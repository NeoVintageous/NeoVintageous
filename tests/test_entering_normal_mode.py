import unittest

from NeoVintageous.vi.constants import _MODE_INTERNAL_NORMAL
from NeoVintageous.vi.constants import MODE_NORMAL
from NeoVintageous.vi.constants import MODE_VISUAL
from NeoVintageous.vi.constants import MODE_VISUAL_LINE
from NeoVintageous.lib.state import State
# from NeoVintageous.vi.actions import vi_r

from NeoVintageous.tests import get_sel
from NeoVintageous.tests import first_sel
from NeoVintageous.tests import ViewTest


class Test_vi_enter_normal_mode__SingleSelection__LeftRoRight(ViewTest):
    def testCaretEndsInExpectedRegion(self):
        self.write('foo bar\nfoo bar\nfoo bar\n')
        self.clear_sel()
        self.add_sel(self.R((1, 0), (1, 3)))

        State(self.view).mode = MODE_VISUAL

        self.view.run_command('_enter_normal_mode', {'mode': MODE_VISUAL})
        self.assertEqual(self.R((1, 2), (1, 2)), first_sel(self.view))


class Test_vi_enter_normal_mode__SingleSelection__RightToLeft(ViewTest):

    def testCaretEndsInExpectedRegion(self):
        self.write(''.join(('foo bar\nfoo bar\nfoo bar\n',)))
        self.clear_sel()
        self.add_sel(self.R((1, 3), (1, 0)))

        self.state.mode = MODE_VISUAL

        self.view.run_command('_enter_normal_mode', {'mode': MODE_VISUAL})
        self.assertEqual(self.R((1, 0), (1, 0)), first_sel(self.view))


class Test_vi_r__SingleSelection__RightToLeft(ViewTest):
    @unittest.skip("must fix this")
    def testCaretEndsInExpectedRegion(self):
        self.write(''.join(('foo bar\nfoo bar\nfoo bar\n',)))
        self.clear_sel()
        self.add_sel(self.R((1, 3), (1, 0)))

        state = State(self.view)
        state.enter_visual_mode()

        # TODO: we should bypass vi_r and define the values directly.
        data = CmdData(state)
        # data = vi_r(data)
        data['action']['args']['character'] = 'X'

        self.view.run_command('vi_run', data)

        self.assertEqual(self.R((1, 0), (1, 0)), first_sel(self.view))
