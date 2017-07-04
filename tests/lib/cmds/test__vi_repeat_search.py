from NeoVintageous.tests.utils import ViewTestCase


class Test__vi_repeat_star_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_forward_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse_twice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_forward_reverse_twice_forward_thrice(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})
        for i in range(0, 2):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})
        for i in range(0, 3):
            self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(4)

        self.view.run_command('_vi_star', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(4, 7), self.Region(12, 15)])


class Test__vi_repeat_octothorp_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_no_partial(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabcxend')
        self.select(4)

        self.view.run_command('_vi_octothorp', {'mode': self.NORMAL_MODE})
        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [self.Region(4, 7), self.Region(12, 15)])


class Test__vi_repeat_slash_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(20)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_slash_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_slash'

        self.assertSelection(4)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])


class Test__vi_repeat_question_mark_InNormalMode(ViewTestCase):

    def test_repeat_forward(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_reverse(self):
        self.write('foo\nabc\nbar\nabc\nmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': True})

        self.assertSelection(4)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])

    def test_repeat_partial(self):
        self.write('foo\nabc\nbar\nabcxmoo\nabc\nend')
        self.select(0)

        self.view.run_command('_vi_question_mark_impl', {'mode': self.NORMAL_MODE, 'search_string': 'abc'})
        self.state.last_buffer_search_command = 'vi_question_mark'

        self.assertSelection(20)

        self.view.run_command('_vi_repeat_buffer_search', {'mode': self.NORMAL_MODE, 'reverse': False})

        self.assertSelection(12)
        self.assertEqual(self.view.get_regions('vi_search'), [
            self.Region(4, 7), self.Region(12, 15), self.Region(20, 23)
        ])
