from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_l_InNormalMode(ViewTestCase):
    def test_can_move_in_normal_mode(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.NORMAL, 'count': 1})
        self.assertEqual(self.R(1, 1), self.first_sel())

    def test_can_move_in_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.NORMAL, 'count': 10})
        self.assertEqual(self.R(10, 10), self.first_sel())

    def test_stops_at_right_end_in_normal_mode(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.NORMAL, 'count': 10000})
        self.assertEqual(self.R(2, 2), self.first_sel())


class Test__vi_l_InInternalNormalMode(ViewTestCase):
    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.INTERNAL_NORMAL, 'count': 1})
        self.assertEqual(self.R(0, 1), self.first_sel())

    def test_can_move_in_internal_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.INTERNAL_NORMAL, 'count': 10})
        self.assertEqual(self.R(0, 10), self.first_sel())

    def test_stops_at_right_end_in_internal_normal_mode(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=0, b=0)

        self.view.run_command('_vi_l', {'mode': modes.INTERNAL_NORMAL, 'count': 10000})
        self.assertEqual(self.R(0, 3), self.first_sel())


class Test__vi_l_InVisualMode(ViewTestCase):
    def test_can_move(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=0, b=1)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(0, 2), self.first_sel())

    def test_can_move_reversed_no_cross_over(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=2, b=0)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(2, 1), self.first_sel())

    def test_can_move_reversed_minimal(self):
        self.write('abc')
        self.clear_sel()
        self.add_sel(a=1, b=0)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(0, 2), self.first_sel())

    def test_can_move_reversed_cross_over(self):
        self.write('foo bar baz')
        self.clear_sel()
        self.add_sel(a=5, b=0)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 5})
        self.assertEqual(self.R(4, 6), self.first_sel())

    def test_can_move_reversed_different_lines(self):
        self.write('foo\nbar\n')
        self.clear_sel()
        self.add_sel(a=5, b=1)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(5, 2), self.first_sel())

    def test_stops_at_eol_different_lines_reversed(self):
        self.write('foo\nbar\n')
        self.clear_sel()
        self.add_sel(a=5, b=3)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 1})
        self.assertEqual(self.R(5, 3), self.first_sel())

    def test_stops_at_eol_different_lines_reversed_large_count(self):
        self.write('foo\nbar\n')
        self.clear_sel()
        self.add_sel(a=5, b=3)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 100})
        self.assertEqual(self.R(5, 3), self.first_sel())

    def test_can_move_with_count(self):
        self.write('foo bar fuzz buzz')
        self.clear_sel()
        self.add_sel(a=0, b=1)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 10})
        self.assertEqual(self.R(0, 11), self.first_sel())

    def test_stops_at_right_end(self):
        self.write('abc\n')
        self.clear_sel()
        self.add_sel(a=0, b=1)

        self.view.run_command('_vi_l', {'mode': modes.VISUAL, 'count': 10000})
        self.assertEqual(self.R(0, 4), self.first_sel())
