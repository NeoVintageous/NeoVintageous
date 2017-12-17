# DEPRECATED These tests can be removed when the functional tests are merged.

from NeoVintageous.tests import unittest


class TestUnimpaired__square_bracket____space__(unittest.ViewTestCase):

    def test_blank_down(self):
        self.write('aaa\nbbb\nccc')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_down'})
        self.assertContent('aaa\nbbb\n\nccc')
        self.assertSelection(4)

    def test_blank_down_cursor_reset_to_first_non_whitespace_character(self):
        self.write('aaa\n    bbb\nccc')
        self.select(10)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_down'})
        self.assertContent('aaa\n    bbb\n\nccc')
        self.assertSelection(8)

    def test_blank_down_with_count(self):
        self.write('aaa\nbbb\nccc')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_down', 'count': 5})
        self.assertContent('aaa\nbbb\n\n\n\n\n\nccc')
        self.assertSelection(4)

    def test_blank_down_with_count_reset_to_first_non_whitespace_character(self):
        self.write('aaa\n    bbb\nccc')
        self.select(10)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_down', 'count': 5})
        self.assertContent('aaa\n    bbb\n\n\n\n\n\nccc')
        self.assertSelection(8)

    def test_blank_up(self):
        self.write('aaa\nbbb\nccc')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_up'})
        self.assertContent('aaa\n\nbbb\nccc')
        self.assertSelection(5)

    def test_blank_up_cursor_reset_to_first_non_whitespace_character(self):
        self.write('aaa\n    bbb\nccc')
        self.select(10)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_up'})
        self.assertContent('aaa\n\n    bbb\nccc')
        self.assertSelection(9)

    def test_blank_up_with_count(self):
        self.write('aaa\nbbb\nccc')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_up', 'count': 3})
        self.assertContent('aaa\n\n\n\nbbb\nccc')
        self.assertSelection(7)

    def test_blank_up_with_count_reset_to_first_non_whitespace_character(self):
        self.write('aaa\n    bbb\nccc')
        self.select(10)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'blank_up', 'count': 3})
        self.assertContent('aaa\n\n\n\n    bbb\nccc')
        self.assertSelection(11)


class TestUnimpaired__square_bracket__e(unittest.ViewTestCase):

    def test_move_down(self):
        self.write('111\n222\n333\n444')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'move_down'})
        self.assertContent('111\n333\n222\n444')
        self.assertSelection(10)

    def test_move_down_with_count(self):
        self.write('111\n222\n333\n444\n555\n666\n777\n888')
        self.select(6)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'move_down', 'count': 5})
        self.assertContent('111\n333\n444\n555\n666\n777\n222\n888')
        self.assertSelection(26)

    def test_move_up(self):
        self.write('111\n222\n333\n444')
        self.select(10)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'move_up'})
        self.assertContent('111\n333\n222\n444')
        self.assertSelection(6)

    def test_move_up_with_count(self):
        self.write('111\n222\n333\n444\n555\n666\n777\n888')
        self.select(26)
        self.view.run_command('_neovintageous_unimpaired', {'action': 'move_up', 'count': 3})
        self.assertContent('111\n222\n333\n777\n444\n555\n666\n888')
        self.assertSelection(14)
