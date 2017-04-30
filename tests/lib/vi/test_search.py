from NeoVintageous.lib.vi.search import find_wrapping

from NeoVintageous.tests.utils import ViewTestCase


class Test_find_wrapping(ViewTestCase):
    def test_can_wrap_around_buffer(self):
        self.write('''xxx
aaa aaa xxx aaa
''')
        self.clear_sel()
        self.add_sel(a=15, b=15)

        # 15 is after the second xxx
        match = find_wrapping(self.view, 'xxx', 15, self.view.size())
        self.assertEqual(match, self.R(0, 3))

    def test_fails_if_search_string_not_present(self):
        self.write('''xxx
aaa aaa xxx aaa
''')
        self.clear_sel()
        self.add_sel(a=15, b=15)

        # 15 is after the second xxx
        match = find_wrapping(self.view, 'yyy', 15, self.view.size())
        self.assertEqual(match, None)

    def test_can_find_next_occurrence(self):
        self.write('''xxx
aaa aaa xxx aaa
''')
        self.clear_sel()
        self.add_sel(a=4, b=4)

        # 4 is the beginning of the second line
        match = find_wrapping(self.view, 'xxx', 4, self.view.size())
        self.assertEqual(match, self.R(12, 15))
