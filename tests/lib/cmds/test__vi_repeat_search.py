from NeoVintageous.lib.vi.utils import modes

from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_repeat_star_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(20, 20))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_forward_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_reverse_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(20, 20))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_forward_reverse_twice_forward_thrice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})
        for i in range(0, 2):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})
        for i in range(0, 3):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_star', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15)])


class Test__vi_repeat_octothorp_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_octothorp', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_octothorp', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(self.R(4, 4))

        self.view.run_command('_vi_octothorp', {'mode': modes.NORMAL})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15)])


class Test__vi_repeat_slash_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertFirstSelection(self.R(4, 4))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertFirstSelection(self.R(4, 4))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(20, 20))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_slash_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertFirstSelection(self.R(4, 4))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])


class Test__vi_repeat_question_mark_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertFirstSelection(self.R(20, 20))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertFirstSelection(self.R(20, 20))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': True})

        self.assertFirstSelection(self.R(4, 4))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(self.R(0, 0))

        self.view.run_command('_vi_question_mark_impl', {'mode': modes.NORMAL, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertFirstSelection(self.R(20, 20))

        self.view.run_command('_vi_repeat_buffer_search', {'mode': modes.NORMAL, 'reverse': False})

        self.assertFirstSelection(self.R(12, 12))
        self.assertEqual(self.view.get_regions('vi_search'), [self.R(4, 7), self.R(12, 15), self.R(20, 23)])
