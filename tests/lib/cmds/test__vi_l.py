from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_l_InNormalMode(ViewTestCase):

    def test_can_move_in_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(1, 1))

    def test_can_move_in_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.NORMAL, 'count': 10})

        self.assertFirstSelection(self.R(10, 10))

    def test_stops_at_right_end_in_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.NORMAL, 'count': 10000})

        self.assertFirstSelection(self.R(2, 2))


class Test__vi_l_InInternalNormalMode(ViewTestCase):

    def test_can_move_in_internal_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.INTERNAL_NORMAL, 'count': 1})

        self.assertFirstSelection(self.R(0, 1))

    def test_can_move_in_internal_normal_mode_with_count(self):
        self.write('foo bar baz')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.INTERNAL_NORMAL, 'count': 10})

        self.assertFirstSelection(self.R(0, 10))

    def test_stops_at_right_end_in_internal_normal_mode(self):
        self.write('abc')
        self.select(0)

        self.view.run_command('_vi_l', {'mode': self.modes.INTERNAL_NORMAL, 'count': 10000})

        self.assertFirstSelection(self.R(0, 3))


class Test__vi_l_InVisualMode(ViewTestCase):

    def test_can_move(self):
        self.write('abc')
        self.select((0, 1))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(0, 2))

    def test_can_move_reversed_no_cross_over(self):
        self.write('abc')
        self.select((2, 0))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(2, 1))

    def test_can_move_reversed_minimal(self):
        self.write('abc')
        self.select((1, 0))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(0, 2))

    def test_can_move_reversed_cross_over(self):
        self.write('foo bar baz')
        self.select((5, 0))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 5})

        self.assertFirstSelection(self.R(4, 6))

    def test_can_move_reversed_different_lines(self):
        self.write('foo\nbar\n')
        self.select((5, 1))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(5, 2))

    def test_stops_at_eol_different_lines_reversed(self):
        self.write('foo\nbar\n')
        self.select((5, 3))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 1})

        self.assertFirstSelection(self.R(5, 3))

    def test_stops_at_eol_different_lines_reversed_large_count(self):
        self.write('foo\nbar\n')
        self.select((5, 3))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 100})

        self.assertFirstSelection(self.R(5, 3))

    def test_can_move_with_count(self):
        self.write('foo bar fuzz buzz')
        self.select((0, 1))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 10})

        self.assertFirstSelection(self.R(0, 11))

    def test_stops_at_right_end(self):
        self.write('abc\n')
        self.select((0, 1))

        self.view.run_command('_vi_l', {'mode': self.modes.VISUAL, 'count': 10000})

        self.assertFirstSelection(self.R(0, 4))
