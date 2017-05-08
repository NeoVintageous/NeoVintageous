from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_slash_InNormalMode(ViewTestCase):
    def test_search_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(0, 0))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(4, 4), self.first_sel())

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(25, 25))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(4, 4), self.first_sel())

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(22, 22))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(4, 4), self.first_sel())

    def test_search_wrap_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')

        self.clear_sel()
        self.add_sel(self.R(27, 27))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(4, 4), self.first_sel())


class Test__vi_question_mark_InNormalMode(ViewTestCase):
    def test_search_wrap_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(0, 0))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(20, 20), self.first_sel())

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(25, 25))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(20, 20), self.first_sel())

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.clear_sel()
        self.add_sel(self.R(12, 12))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(4, 4), self.first_sel())

    def test_search_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')

        self.clear_sel()
        self.add_sel(self.R(27, 27))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.assertEqual(self.R(20, 20), self.first_sel())
