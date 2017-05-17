"""Tests for o motion (visual kind)."""

from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_visual_o_InNormalMode(ViewTestCase):

    def test_doesnt_do_anything(self):
        self.write('abc')
        self.select(self.R((0, 2), (0, 0)))

        self.view.run_command('_vi_visual_o', {'mode': modes.NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 0))


class Test__vi_visual_o_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.select(self.R((0, 2), (0, 0)))

        self.view.run_command('_vi_visual_o', {'mode': modes.INTERNAL_NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 0))


class Test__vi_visual_o_InVisualMode(ViewTestCase):

    def test_can_move(self):
        self.write('abc')
        self.select(self.R(0, 2))

        self.view.run_command('_vi_visual_o', {'mode': modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 0))


class Test__vi_visual_o_InVisualLineMode(ViewTestCase):

    def test_can_move(self):
        self.write('abc\ndef')
        self.select(self.R(0, 4))

        self.view.run_command('_vi_visual_o', {'mode': modes.VISUAL_LINE, 'count': 1})

        self.assertFirstSelection(self.R(4, 0))
