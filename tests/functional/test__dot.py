# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

from NeoVintageous.tests import unittest


class Test_dot(unittest.FunctionalTestCase):

    @unittest.mock_bell()
    def test_nothing_to_repeat_should_do_nothing_and_invoke_bell(self):
        self.normal('fi|zz')
        self.feed('.')
        self.assertNormal('fi|zz')
        self.assertBell()

    def test_n_repeat_dw(self):
        self.normal('one |two three four five six seven')
        self.feed('dw')
        self.assertNormal('one |three four five six seven')
        self.feed('.')
        self.assertNormal('one |four five six seven')
        self.feed('3.')
        self.assertNormal('one |seven')

    def test_v_repeat_d(self):
        self.normal('one |two three four five six seven')
        self.feed('v')
        self.feed('w')
        self.feed('d')
        self.assertNormal('one |hree four five six seven')
        self.feed('.')
        self.assertNormal('one |four five six seven')
        self.feed('2.')
        self.assertNormal('one |five six seven')  # visual repeats are ignored in Vim
        self.feed('3.')
        self.assertNormal('one |six seven')  # visual repeats are ignored in Vim

    @unittest.mock_bell()
    def test_trying_to_repeat_normal_mode_commands_in_visual_mode_should_invoke_bell(self):
        self.normal('one |two three four')
        self.feed('dw')
        self.feed('v')
        self.feed('.')
        self.assertVisual('one |t|hree four')
        self.assertBell()

    @unittest.mock.patch('sublime.View.command_history')
    def test_repeat_insert(self, command_history):
        command_history.return_value = ('insert', {'characters': 'buzz'}, 1)
        self.normal('fizz  |x')
        self.feed('i')
        self.assertInsert('fizz  |x')
        self.feed('<Esc>')
        self.assertNormal('fizz | x')
        self.feed('.')
        self.assertNormal('fizz buzz| x')

    @unittest.mock.patch('sublime.View.command_history')
    def test_repeat_append_sequence(self, command_history):
        command_history.return_value = ('sequence', {'commands': [
            ['nv_vi_a', {'count': 1, 'mode': 'mode_internal_normal'}],
            ['insert', {'characters': 'buzz'}]]}, 1)

        self.normal('fizz | x')
        self.feed('i')
        self.assertInsert('fizz | x')
        self.feed('<Esc>')
        self.assertNormal('fizz|  x')
        self.feed('.')
        self.assertNormal('fizz buzz| x')

    @unittest.mock.patch('sublime.View.command_history')
    def test_dot_repeat_insert_sequence(self, command_history):
        command_history.return_value = ('sequence', {'commands': [
            ['insert', {'characters': 'buzzz'}],
            ['left_delete', None]]}, 1)
        self.normal('fizz  |x')
        self.feed('i')
        self.assertInsert('fizz  |x')
        self.feed('<Esc>')
        self.assertNormal('fizz | x')
        self.feed('.')
        self.assertNormal('fizz buzz| x')

    def test_repeat_visual_operation_x(self):
        self.visual('fizz |buzz|fizzbuzz')
        self.feed('x')
        self.assertNormal('fizz |fizzbuzz')
        self.feed('.')
        self.assertNormal('fizz |buzz')
        self.visual('x\nf|izz\nbuz|z\nping\npong\nx')
        self.feed('x')
        self.assertNormal('x\nf|z\nping\npong\nx')
        self.feed('.')
        self.assertNormal('x\nf|g\npong\nx')

    def test_repeat_visual_line_operation_x(self):
        self.vline('x\n|fizz\n|buzz\nx\n')
        self.feed('x')
        self.assertNormal('x\n|buzz\nx\n')
        self.feed('.')
        self.assertNormal('x\n|x\n')
        self.vline('x\n|fizz\nbuzz\n|ping\npong\nx\n')
        self.feed('x')
        self.assertNormal('x\n|ping\npong\nx\n')
        self.feed('.')
        self.assertNormal('x\n|x\n')

    @unittest.mock_bell()
    def test_repeat_rings_bell_in_visual_mode(self):
        self.normal('fi|xzz')
        self.feed('x')
        self.assertNormal('fi|zz')
        self.feed('v')
        self.assertVisual('fi|z|z')
        self.feed('.')
        self.assertVisual('fi|z|z')
        self.assertBell()

    @unittest.mock_bell()
    @unittest.mock.patch('sublime.View.is_dirty')
    def test_dot_rings_bell_when_nothing_to_repeat(self, is_dirty=None):
        is_dirty.return_value = False
        self.normal('fizz  |x')
        self.feed('i')
        self.feed('<Esc>')
        self.feed('.')
        self.assertNormal('fizz | x')
        self.assertBell()

    def test_issue_10_dot_repeat(self):
        self.normal('|abcdefg\nabcdefg\n')
        self.feed('v')
        self.feed('2l')
        self.feed('c')
        self.assertInsert('|defg\nabcdefg\n')
        self.feed('<Esc>')
        self.feed('j')
        self.assertNormal('defg\n|abcdefg\n')
        self.feed('.')
        self.assertNormal('defg\n|defg\n')
        self.normal('x|abcdefg\nabcdefghijkl\n')
        self.feed('v')
        self.feed('2l')
        self.feed('c')
        self.view.run_command('insert', {'characters': 'fizz'})
        self.assertInsert('xfizz|defg\nabcdefghijkl\n')
        self.feed('<Esc>')
        self.feed('j')
        self.assertNormal('xfizzdefg\nabcd|efghijkl\n')
        self.feed('.')
        # self.assertNormal('xfizzdefg\nabcdfizz|hijkl\n')
