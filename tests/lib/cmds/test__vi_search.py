from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_slash_InNormalMode(ViewTestCase):

    def test_search_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(4)

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(25)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(4)

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(22)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(4)

    def test_search_wrap_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(27)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(4)


class Test__vi_question_mark_InNormalMode(ViewTestCase):

    def test_search_wrap_begin(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(20)

    def test_search_wrap(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(25)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(20)

    def test_search_wrap_mid_match(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(12)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(4)

    def test_search_end(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(27)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})

        self.assertSelection(20)
