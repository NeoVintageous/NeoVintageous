# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

from NeoVintageous.nv.settings import set_reset_during_init


@unittest.mock.patch.dict('NeoVintageous.nv.session._session', {})
@unittest.mock.patch('NeoVintageous.nv.session.save_session', unittest.mock.Mock())
class TestFeedKey(unittest.ResetRegisters, unittest.ResetCommandLineOutput, unittest.FunctionalTestCase):

    def feedkey(self, key):
        self.view.window().run_command('nv_feed_key', {'key': key})  # type: ignore[union-attr]

    def feedkeys(self, keys):
        for key in keys:
            self.view.window().run_command('nv_feed_key', {'key': key})  # type: ignore[union-attr]

    def setUp(self):
        super().setUp()
        self.set_setting('use_sys_clipboard', False)

    def tearDown(self):
        super().tearDown()
        self.resetMacros()

    def test_malformed_visual_selections_are_auto_fixed(self):
        self.visual('fi|zz| buzz')
        self.setNormalMode()
        self.feedkey('w')
        self.assertVisual('fi|zz b|uzz')

    def test_malformed_multiple_visual_selections_are_auto_fixed(self):
        self.visual('fi|zz| buzz fi|zz| buzz')
        self.setNormalMode()
        self.feedkey('w')
        self.assertVisual('fi|zz b|uzz fi|zz b|uzz')

    def test_esc(self):
        self.visual('f|izz b|uzz')
        self.feedkey('<esc>')
        self.assertNormal('fizz |buzz')
        self.assertStatusLineIsNormal()

    def test_esc_key_should_be_case_insensitive(self):
        for key in ('<Esc>', '<esc>', '<ESC>'):
            self.visual('f|izz b|uzz')
            self.feedkey(key)
            self.assertNormal('fizz |buzz')

    def test_esc_in_select_mode_exits_multiple_selection(self):
        self.set_setting('multi_cursor_exit_from_visual_mode', True)
        self.vselect('f|iz|z\nb|uz|z\n')
        self.feedkey('<esc>')
        self.assertNormal('f|izz\nbuzz\n')
        self.set_setting('multi_cursor_exit_from_visual_mode', False)
        self.vselect('f|iz|z\nb|uz|z\n')
        self.feedkey('<esc>')
        self.assertNormal('f|izz\nb|uzz\n')
        self.set_setting('multi_cursor_exit_from_visual_mode', True)
        self.vselect('f|iz|z\nb|uz|z\n')
        self.feedkey('<esc>')
        self.assertNormal('f|izz\nbuzz\n')

    def test_motion(self):
        self.normal('fi|zz buzz')
        self.feedkey('w')
        self.assertNormal('fizz |buzz')

    def test_count_motion(self):
        self.normal('fi|zz buzz three four')
        self.feedkey('3')
        self.feedkey('w')
        self.assertNormal('fizz buzz three |four')

    def test_visual_motion(self):
        self.visual('f|iz|z buzz')
        self.feedkey('w')
        self.assertVisual('f|izz b|uzz')
        self.assertStatusLineIsVisual()

    def test_zero_is_not_a_count(self):
        self.normal('x\n  fi|zz')
        self.feedkey('0')
        self.assertNormal('x\n|  fizz')

    def test_double_digit_count(self):
        self.normal('|1234567890123456789012345')
        self.feedkey('2')
        self.feedkey('3')
        self.feedkey('l')
        self.assertNormal('12345678901234567890123|45')

    def test_double_digit_count_ending_in_zero(self):
        self.normal('|1234567890123456789012345')
        self.feedkey('2')
        self.feedkey('0')
        self.feedkey('l')
        self.assertNormal('12345678901234567890|12345')

    def test_namespaced_motion(self):
        self.normal('1\n2\nf|izz')
        self.feedkey('g')
        self.assertStatusLineEqual('g')
        self.assertNormal('1\n2\nf|izz')
        self.feedkey('g')
        self.assertNormal('|1\n2\nfizz')
        self.assertStatusLineIsNormal()

    def test_count_namespaced_motion(self):
        self.normal('1\n2\n3\nf|izz')
        self.feedkey('2')
        self.feedkey('g')
        self.assertStatusLineEqual('2g')
        self.assertNormal('1\n2\n3\nf|izz')
        self.feedkey('g')
        self.assertNormal('1\n|2\n3\nfizz')
        self.assertStatusLineIsNormal()

    def test_operator(self):
        self.normal('f|izz')
        self.feedkey('~')
        self.assertNormal('fI|zz')
        self.assertStatusLineIsNormal()

    def test_operator_motion(self):
        self.normal('fi|zz buzz')
        self.feedkey('d')
        self.assertStatusLineEqual('d')
        self.feedkey('w')
        self.assertNormal('fi|buzz')
        self.assertStatusLineIsNormal()

    def test_visual_operator(self):
        self.visual('fi|zz bu|zz')
        self.feedkey('d')
        self.assertNormal('fi|zz')
        self.assertStatusLineIsNormal()
        self.assertRegisters('"-', 'zz bu')
        self.assertRegistersEmpty('01')

    def test_count_operator_motion(self):
        self.normal('fi|zz buzz three four')
        self.feedkey('3')
        self.feedkey('d')
        self.assertStatusLineEqual('3d')
        self.feedkey('w')
        self.assertNormal('fi|four')
        self.assertStatusLineIsNormal()
        self.assertRegisters('"-', 'zz buzz three ')
        self.assertRegistersEmpty('01')

    def test_operator_operator_dd(self):
        self.normal('1\nfi|zz\n2\n3')
        self.feedkey('d')
        self.feedkey('d')
        self.assertNormal('1\n|2\n3')
        self.assertLinewiseRegisters('"1', 'fizz\n')
        self.assertRegistersEmpty('-02')
        self.assertStatusLineIsNormal()

    def test_operator_operator_cc(self):
        self.normal('1\nfi|zz\n2\n3')
        self.feedkey('c')
        self.feedkey('c')
        self.assertInsert('1\n|\n2\n3')
        self.assertLinewiseRegisters('"1', 'fizz\n')
        self.assertRegistersEmpty('-02')
        self.assertStatusLineIsInsert()

    def test_operator_operator_equal_equal(self):
        self.settings().set('translate_tabs_to_spaces', True)
        self.settings().set('tab_size', 4)
        self.normal('1\nfi|zz\n2')
        self.feedkey('>')
        self.feedkey('>')
        self.assertNormal('1\n    |fizz\n2')
        self.assertRegistersEmpty('"-012abc')
        self.assertStatusLineIsNormal()

    def test_motion_and_operator_counts_are_multiplied(self):
        self.normal('o|ne two three four five six seven')
        self.feedkey('3')
        self.feedkey('d')
        self.feedkey('2')
        self.assertStatusLineEqual('3d2')
        self.feedkey('w')
        self.assertNormal('o|seven')
        self.assertStatusLineIsNormal()
        self.assertRegisters('"-', 'ne two three four five six ')
        self.assertRegistersEmpty('01')

    def test_register(self):
        self.normal('fi|zz buzz')
        self.feedkey('"')
        self.feedkey('c')
        self.feedkey('d')
        self.assertStatusLineEqual('"cd')
        self.feedkey('w')
        self.assertNormal('fi|buzz')
        self.assertStatusLineIsNormal()
        self.assertRegisters('"c', 'zz ')
        self.assertRegistersEmpty('-012abde')

    def test_undo_redo(self):
        self.normal('fizz\n|xyz\nbuzz\nbong')
        self.feedkeys('dd')
        self.assertNormal('fizz\n|buzz\nbong')
        self.feedkey('u')
        self.assertNormal('fizz\n|xyz\nbuzz\nbong')
        self.feedkey('<C-r>')
        self.assertNormal('fizz\n|buzz\nbong')

    @unittest.mock_bell()
    def test_unknown_operator_motion_invokes_bell(self):
        self.normal('fi|zz')
        self.feedkey('d')
        self.feedkey('o')
        self.assertNormal('fi|zz')
        self.assertStatusLineIsNormal()
        self.assertRegistersEmpty('"-012abc')
        self.assertBell()

    @unittest.mock_bell()
    def test_unknown_visual_operator_motion_invokes_bell_but_stays_in_visual(self):
        self.visual('fi|zz bu|zz')
        self.feedkey('g')
        self.feedkey('y')
        self.assertVisual('fi|zz bu|zz')
        self.assertStatusLineIsVisual()
        self.assertRegistersEmpty('"-012abc')
        self.assertBell()

    def test_malformed_visual_selection_is_auto_corrected_by_feed(self):
        self.normal('fi|zz buzz fizz')
        self.select((2, 7))
        self.feedkey('w')
        self.assertVisual('fi|zz buzz f|izz')

    def test_input_collecting(self):
        self.normal('fi|zz buzz')
        self.feedkey('f')
        self.assertNormal('fi|zz buzz')
        self.assertStatusLineEqual('f')
        self.feedkey('u')
        self.assertNormal('fizz b|uzz')
        self.assertStatusLineIsNormal()

    def test_input_collecting_replace(self):
        self.normal('fi|zz')
        self.feedkey('R')
        self.assertReplace('fi|zz')
        self.assertStatusLineIsReplace()

    def test_record(self):
        self.normal('fi|zz buzz fizz buzz fizz buzz')
        self.feedkey('q')
        self.assertStatusLineEqual('q')
        self.feedkey('n')
        self.assertStatusLineEqual('recording @n')
        self.feedkey('f')
        self.feedkey('b')
        self.feedkey('q')
        self.assertNormal('fizz |buzz fizz buzz fizz buzz')
        self.assertStatusLineEqual('')
        self.feedkey('@')
        self.assertStatusLineEqual('@')
        self.feedkey('n')
        self.assertNormal('fizz buzz fizz |buzz fizz buzz')
        self.assertStatusLineEqual('')
        self.feedkey('@')
        self.assertStatusLineEqual('@')
        self.feedkey('@')
        self.assertNormal('fizz buzz fizz buzz fizz |buzz')
        self.assertStatusLineEqual('')

    def test_record_delete_operation(self):
        self.normal('fizz buzz fizz buzz fizz |buzz')
        self.feedkey('q')
        self.feedkey('x')
        self.assertStatusLineEqual('recording @x')
        self.feedkey('2')
        self.feedkey('d')
        self.feedkey('b')
        self.feedkey('q')
        self.assertNormal('fizz buzz fizz |buzz')
        self.assertStatusLineEqual('')
        self.feedkey('@')
        self.feedkey('x')
        self.assertNormal('fizz |buzz')
        self.assertStatusLineEqual('')

    def test_record_xpos_motion(self):
        self.normal('fi|zz\nbuzz\nfizz\nbuzz\nfizz\nbuzz')
        self.feedkey('q')
        self.feedkey('x')
        self.feedkey('j')
        self.feedkey('q')
        self.assertNormal('fizz\nbu|zz\nfizz\nbuzz\nfizz\nbuzz')
        self.feedkey('@')
        self.feedkey('x')
        self.assertNormal('fizz\nbuzz\nfi|zz\nbuzz\nfizz\nbuzz')
        self.feedkey('2')
        self.feedkey('@')
        self.feedkey('x')
        self.assertNormal('fizz\nbuzz\nfizz\nbuzz\nfi|zz\nbuzz')

    def test_record_xpos_delete_motion_operation(self):
        self.normal('one\n|two\nthree\nfour\nfive\nsix\nseven')
        self.feedkey('q')
        self.feedkey('x')
        self.feedkey('d')
        self.feedkey('j')
        self.feedkey('q')
        self.assertNormal('one\n|four\nfive\nsix\nseven')
        self.feedkey('@')
        self.feedkey('x')
        self.assertNormal('one\n|six\nseven')

    def test_marks(self):
        for key in ('\'', '`'):
            self.normal('1\n2\n|fizz\n4\n5\n6\n7')
            self.feedkeys('mo')
            self.feedkeys('6G')  # go to and mark line 6
            self.feedkeys('mt')
            self.feedkeys(key + 'o')  # goto mark a
            self.assertNormal('1\n2\n|fizz\n4\n5\n6\n7')
            self.feedkeys(key + 't')  # goto mark b
            self.assertNormal('1\n2\nfizz\n4\n5\n|6\n7')
            self.feedkey('k')  # go up a line
            self.feedkeys(key + 'o')  # goto mark a
            self.assertNormal('1\n2\n|fizz\n4\n5\n6\n7')
            self.feedkey('v')  # enter Visual
            self.feedkeys(key + 't')    # goto mark b
            self.assertVisual('1\n2\n|fizz\n4\n5\n6|\n7')

    def test_mark_move_to_first_non_blank(self):
        self.normal('1\n2\n|    fizz\n4\n')
        self.feedkeys('mo')
        self.feedkeys('1G')
        self.feedkeys('`o')
        self.assertNormal('1\n2\n|    fizz\n4\n')
        self.normal('1\n2\n|    fizz\n4\n')
        self.feedkeys('mo')
        self.feedkeys('1G')
        self.feedkeys('\'o')
        self.assertNormal('1\n2\n    |fizz\n4\n')

    def test_visual_marks(self):
        for key in ('\'', '`'):
            self.normal('one\ntwo\nthree\n|four\nfive')
            self.feedkeys('mo')
            self.feedkeys('2k')
            self.feedkeys('mt')
            self.feedkey('v')
            self.assertVisual('one\n|t|wo\nthree\nfour\nfive')
            self.feedkeys(key + 'o')
            self.assertVisual('one\n|two\nthree\nf|our\nfive')
            self.feedkeys(key + 't')
            self.assertVisual('one\n|t|wo\nthree\nfour\nfive')
            self.feedkeys('gg')
            self.assertRVisual('|one\nt|wo\nthree\nfour\nfive')
            self.feedkeys(key + 'o')
            self.assertVisual('one\n|two\nthree\nf|our\nfive')

    def test_visual_mark_includes_first_non_blank(self):
        self.normal('1\n2\n|    fizz\n4\n')
        self.feedkeys('mo')
        self.feedkeys('1G')
        self.feedkeys('v')
        self.feedkeys('\'o')
        self.assertVisual('|1\n2\n    f|izz\n4\n')

    def test_visual_mark_includes_first_column(self):
        self.normal('1\n2\n|    fizz\n4\n')
        self.feedkeys('mo')
        self.feedkeys('1G')
        self.feedkeys('v')
        self.feedkeys('`o')
        self.assertVisual('|1\n2\n |   fizz\n4\n')

    def test_mark_operations(self):
        for key in ('\'', '`'):
            self.normal('1\n|2\n3\n4\n5\n6\n7')
            self.feedkey('m')
            self.feedkey('o')
            self.feedkey('3')
            self.feedkey('j')
            self.feedkey('d')
            self.feedkey(key)
            self.feedkey('o')
            self.assertNormal('1\n|6\n7')
            self.normal('1\n2\n3\n4\n|5\n6\n7')
            self.feedkey('m')
            self.feedkey('o')
            self.feedkey('3')
            self.feedkey('k')
            self.feedkey('d')
            self.feedkey(key)
            self.feedkey('o')
            self.assertNormal('1\n|\n6\n7')

    @unittest.mock_mappings()
    def test_substitute_marked_ranges(self):
        for key in ('\'', '`'):
            self.normal('1this\n2th|is\n3this\n4this\n5this\n6this\n7this')
            self.feedkey('m')
            self.feedkey('o')
            self.feedkey('3')
            self.feedkey('j')
            self.feedkey('m')
            self.feedkey('t')
            self.feed(':\'o,\'ts/this/that/')
            self.assertNormal('1this\n2that\n3that\n4that\n|5that\n6this\n7this')

    @unittest.mock_bell()
    @unittest.mock_mappings((unittest.NORMAL, 'l', 'w'))
    def test_can_count_user_mapping(self):
        self.normal('|fizz buzz fizz')
        self.feedkeys('2l')
        self.assertNormal('fizz buzz |fizz')

    @unittest.mock_bell()
    @unittest.mock_mappings((unittest.NORMAL, '9h', 'b'))
    def test_can_resolve_digit_user_mapping(self):
        self.normal('fizz buzz |fizz')
        self.feedkeys('9h')
        self.assertNormal('fizz |buzz fizz')

    @unittest.mock_bell()
    @unittest.mock_mappings(
        (unittest.NORMAL, ',a', '3l'),
        (unittest.VISUAL, ',a', '3l'),
        (unittest.OPERATOR_PENDING, ',a', '3l'),
        (unittest.VISUAL, ',ba', ':sort iu<CR>'),
        (unittest.NORMAL, ',bb', 'vi]:sort iu<CR>'),
        (unittest.NORMAL, ',c', 'vfx'),
        (unittest.NORMAL, ',d', 'f'),
        (unittest.NORMAL, ',e', 'wi'),
        (unittest.NORMAL, ',f', 'wi<Esc>'),
        (unittest.NORMAL, ',g', 'wifizz<Space>'),
        (unittest.NORMAL, ',h', '/foo<CR>cwfizz<Esc>'),
        (unittest.NORMAL, ',i', 'ifizz<Esc>fz'),
        (unittest.NORMAL, ',j', 'ifizz<Esc>f'),
        (unittest.NORMAL, ',k', 'ca'),
        (unittest.NORMAL, '2l', 'w'),
        (unittest.NORMAL, '""', 'b'),
    )
    def test_process_notation(self):
        self.normal('|fizz buzz')
        self.feedkeys(',a')
        self.assertNormal('fiz|z buzz')
        self.visual('f|iz|z buzz')
        self.feedkeys(',a')
        self.assertVisual('f|izz b|uzz')
        self.normal('fiz|z buzz')
        self.feedkeys('d,a')
        self.assertNormal('fiz|uzz')
        self.visual('3\n|5\n1\n5\n1\n4\n4|\n2\n')
        self.feedkeys(',ba')
        self.assertNormal('3\n|1\n4\n5\n2\n')
        self.normal('9\n3\n3\n[\n1\n5\n|1\n4\n4\n]\n1\n2')
        self.feedkeys(',bb')
        self.assertNormal('9\n3\n3\n[\n|1\n4\n5\n]\n1\n2')
        self.normal('f|izzxbuzz')
        self.feedkeys(',c')
        self.assertVisual('f|izzx|buzz')
        self.normal('f|izzxbuzz')
        self.feedkeys(',dx')
        self.assertNormal('fizz|xbuzz')
        self.normal('fiz|z buzz')
        self.feedkeys(',e')
        self.assertInsert('fizz |buzz')
        self.normal('fiz|z buzz')
        self.feedkeys(',f')
        self.assertNormal('fizz |buzz')
        self.normal('f|oo buzz')
        self.feedkeys(',g')
        self.assertInsert('foo fizz |buzz')
        self.normal('o|ne\ntwo\nfoo buzz\nthree')
        self.feedkeys(',h')
        self.assertNormal('one\ntwo\nfizz| buzz\nthree')
        self.normal('| buzz')
        self.feedkeys(',i')
        self.assertNormal('fizz bu|zz')
        self.normal('| buzz')
        self.feedkeys(',ju')
        self.assertNormal('fizz b|uzz')
        self.normal('|foo buzz')
        self.feedkeys(',kw')
        self.assertInsert('| buzz')
        self.assertNoBell()
        self.normal('|fizz buzz')
        self.feedkeys('2l')
        self.assertNormal('fizz |buzz')
        self.normal('fizz bu|zz')
        self.feedkeys('""')
        self.assertNormal('fizz |buzz')
        self.assertNoBell()

    # Breaks ci https://github.com/NeoVintageous/NeoVintageous/actions/runs/7969839600/job/21756321760
    # @unittest.mock_ui(em_width=10)
    # @unittest.mock_mappings((unittest.NORMAL, 'a', 'zl'))
    # @unittest.mock.patch('sublime.View.set_viewport_position')
    # def test_can_map_zl_with_count(self, position):
    #     self.normal('fizz| buzz')
    #     self.feedkey('a')
    #     position.assert_called_with((10.0, 0.0))
    #     self.feedkey('5')
    #     self.feedkey('a')
    #     position.assert_called_with((50.0, 0.0))

    @unittest.mock_bell()
    @unittest.mock_mappings(
        (unittest.NORMAL, ',m1', ':fizz'),
        (unittest.NORMAL, ',m2', ':.yank<CR>2jp'),
    )
    @unittest.mock.patch('NeoVintageous.nv.commands.Cmdline.prompt')
    def test_process_cmdline_prompt_mapping(self, cmdline_prompt):
        self.normal('|fizz buzz')
        self.feedkey(',m1')
        cmdline_prompt.assert_called_once_with('fizz')
        self.normal('1\nfi|zz\n3\n4\n5\n6')
        self.feedkey(',m2')
        self.assertNormal('1\nfizz\n3\n4|fizz\n\n5\n6')
        set_reset_during_init(self.view, True)

    @unittest.mock_commands('nv_vi_slash')
    def test_slash_search_opens_input_panel(self):
        self.normal('|fizz')
        self.feedkey('/')
        self.assertRunCommand('nv_vi_slash')

    @unittest.mock_commands('nv_vi_question_mark')
    def test_question_search_opens_input_panel(self):
        self.normal('|fizz')
        self.feedkey('?')
        self.assertRunCommand('nv_vi_question_mark')
