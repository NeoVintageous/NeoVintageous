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

noop_targets = 'wWsp'

invalid_targets = '20qe'

quote_targets = '\'"`'

other_targets = '.,-_,.;:+-=~*#\\&$'

punctuation_targets = 'b()B{}r[]a<>'

punctuation_targets_data = (
    # (Open, Close, Alias)
    ('(', ')', 'b'),
    ('{', '}', 'B'),
    ('[', ']', 'r'),
    ('<', '>', 'a'))

tag_targets_data = (
    ('<div>', '</div>'),
    ('<i>', '</i>'))

invalid_tag_targets_data = (
    ('i', 'i'),
    ('<i>', '<i>'),
    ('<i>', 'i'),
    ('i', '</i>'),
    ('i>', '<i'),
    ('<i', 'i>'),
    ('[i]', '[/i]'),
    ('<div>', '<x/div>'),
    ('<div>', '<\\/div>'),
    ('<div>', '<\\/div>'))


class TestSurround_ds(unittest.FunctionalTestCase):

    def test_quote_marks(self):
        self.eq('x"a|bc"y', 'ds"', 'x|abcy')
        self.eq('x`a|bc`y', 'ds`', 'x|abcy')
        self.eq("x'a|bc'y", "ds'", 'x|abcy')

    def test_punctuation_marks_and_their_aliases(self):
        self.eq('x(a|bc)y', 'ds(', 'x|abcy')
        self.eq('x(a|bc)y', 'ds)', 'x|abcy')
        self.eq('x(a|bc)y', 'dsb', 'x|abcy')
        self.eq('x{a|bc}y', 'ds{', 'x|abcy')
        self.eq('x{a|bc}y', 'ds}', 'x|abcy')
        self.eq('x{a|bc}y', 'dsB', 'x|abcy')
        self.eq('x[a|bc]y', 'ds[', 'x|abcy')
        self.eq('x[a|bc]y', 'ds]', 'x|abcy')
        self.eq('x[a|bc]y', 'dsr', 'x|abcy')
        self.eq('x<a|bc>y', 'ds<', 'x|abcy')
        self.eq('x<a|bc>y', 'ds>', 'x|abcy')
        self.eq('x<a|bc>y', 'dsa', 'x|abcy')

    def test_other_marks(self):
        self.eq('x.a|bc.y', 'ds.', 'x|abcy')
        self.eq('x,a|bc,y', 'ds,', 'x|abcy')
        self.eq('x-a|bc-y', 'ds-', 'x|abcy')
        self.eq('x_a|bc_y', 'ds_', 'x|abcy')

    def test_should_work_when_cursor_is_on_target(self):
        self.eq('x|"abc"y', 'ds"', 'x|abcy')
        self.eq('x|`abc`y', 'ds`', 'x|abcy')
        self.eq("x|'abc'y", "ds'", 'x|abcy')
        self.eq('x|.abc.y', 'ds.', 'x|abcy')
        self.eq('x|,abc,y', 'ds,', 'x|abcy')
        self.eq('x|-abc-y', 'ds-', 'x|abcy')
        self.eq('x|_abc_y', 'ds_', 'x|abcy')
        self.eq('x|(abc)y', 'ds(', 'x|abcy')
        self.eq('x|(abc)y', 'ds)', 'x|abcy')
        self.eq('x|(abc)y', 'dsb', 'x|abcy')
        self.eq('x|{abc}y', 'ds{', 'x|abcy')
        self.eq('x|{abc}y', 'ds}', 'x|abcy')
        self.eq('x|{abc}y', 'dsB', 'x|abcy')
        self.eq('x|[abc]y', 'ds[', 'x|abcy')
        self.eq('x|[abc]y', 'ds]', 'x|abcy')
        self.eq('x|[abc]y', 'dsr', 'x|abcy')
        self.eq('x|<abc>y', 'ds<', 'x|abcy')
        self.eq('x|<abc>y', 'ds>', 'x|abcy')
        self.eq('x|<abc>y', 'dsa', 'x|abcy')

    def test_quotes_and_other_marks_should_only_be_search_on_current_line(self):
        self.eq('x"\na|bc"y', 'ds"', 'x"\na|bc"y')
        self.eq('x"\na|bc\n"y', 'ds"', 'x"\na|bc\n"y')
        self.eq('x"a|bc\n"y', 'ds"', 'x"a|bc\n"y')
        self.eq('x"a|bc\n\n"y', 'ds"', 'x"a|bc\n\n"y')
        self.eq('x"\n\na|bc\n\n"y', 'ds"', 'x"\n\na|bc\n\n"y')
        self.eq('x"\n\na|bc"y', 'ds"', 'x"\n\na|bc"y')

    def test_multiple_cursors(self):
        self.eq('x"a|c"\n"d|c"y', 'ds"', 'x|ac\n|dcy')

    def test_should_delete_targets(self):
        expected = 'x |abc y'
        for t in quote_targets + other_targets:
            self.eq('x {0}a|bc{0} y'.format(t), 'ds' + t, expected)

    def test_should_delete_targets_for_punctuation(self):
        expected = 'x |abc y'
        for o, c, a in punctuation_targets_data:
            seed = 'x {}a|bc{} y'.format(o, c)
            self.eq(seed, 'ds' + o, expected)  # Open target
            self.eq(seed, 'ds' + c, expected)  # Close target
            self.eq(seed, 'ds' + a, expected)  # Close alias target

    def test_should_do_nothing_when_no_target_is_found(self):
        for t in quote_targets + other_targets + punctuation_targets + noop_targets + invalid_targets:
            self.eq('x a|bc y', 'ds' + t, 'x a|bc y')

    def test_invalid_targets_should_do_nothing(self):
        for t in invalid_targets:
            self.eq('x {0}a|b{0} y'.format(t), 'ds' + t)

    def test_noop_targets_should_do_nothing(self):
        for t in noop_targets:
            self.eq('x {0}a|b{0} y'.format(t), 'ds' + t)

    def test_should_do_nothing_when_only_one_target_is_found(self):
        for t in quote_targets + other_targets + punctuation_targets + noop_targets + invalid_targets:
            self.eq('x {}a|bc y'.format(t), 'ds' + t)
            self.eq('x a|bc{} y'.format(t), 'ds' + t)

    def test_should_not_strip_contained_whitespace(self):
        expected = 'x  |   ab     y'
        for t in quote_targets + other_targets:
            self.eq('x  {0}   a|b    {0} y'.format(t), 'ds' + t, expected)

    def test_should_not_strip_contained_whitespace_for_punctuation(self):
        expected = 'x  |   ab     y'
        for o, c, a in punctuation_targets_data:
            seed = 'x  {}   a|b    {} y'.format(o, c)
            self.eq(seed, 'ds' + c, expected)  # Close target
            self.eq(seed, 'ds' + a, expected)  # Close alias target

    def test_nested_punctuation_marks(self):
        for o, c, a in punctuation_targets_data:
            self.eq('x {0} fi|zz{0}{1} {1} x'.format(o, c), 'ds' + o, 'x |fizz{0}{1} x'.format(o, c))
            self.eq('x |{0} fizz{0}{1} {1} x'.format(o, c), 'ds' + o, 'x |fizz{0}{1} x'.format(o, c))
            self.eq('x {0} fizz|{0}{1} {1} x'.format(o, c), 'ds' + o, 'x {0} fizz| {1} x'.format(o, c))

    def test_punctuation_open_targets_should_strip_contained_whitespace(self):
        for t in punctuation_targets_data:
            self.eq('x {}    a|b    {} y'.format(t[0], t[1]), 'ds' + t[0], 'x |ab y')

    def test_targets_that_should_only_search_the_current_line(self):
        for t in quote_targets + other_targets:
            self.eq('x {0}\na|b{0} y'.format(t), 'ds' + t)
            self.eq('x {0}a|b\n{0} y'.format(t), 'ds' + t)
            self.eq('x {0}\na|b\n{0} y'.format(t), 'ds' + t)

    def test_quote_and_other_targets_should_work_when_cursor_is_on_begin_target(self):
        for t in quote_targets + other_targets:
            self.eq('|{0}abc{0}'.format(t), 'ds' + t, '|abc')
            self.eq('x |{0}abc{0} y'.format(t), 'ds' + t, 'x |abc y')

    def test_quote_and_other_targets_should_work_when_cursor_is_on_begin_target_for_punctuation(self):
        for o, c, a in punctuation_targets_data:
            self.eq('|{}abc{}'.format(o, c), 'ds' + o, '|abc')  # Open target
            self.eq('|{}abc{}'.format(o, c), 'ds' + c, '|abc')  # Close target
            self.eq('|{}abc{}'.format(o, c), 'ds' + a, '|abc')  # Close alias target

    def test_quote_and_other_targets_should_work_when_cursor_is_on_end_target(self):
        for t in punctuation_targets_data:
            self.eq('{}abc|{}'.format(t[0], t[1]), 'ds' + t[0], '|abc')
            self.eq('{}abc|{}'.format(t[0], t[1]), 'ds' + t[1], '|abc')
            self.eq('{}abc|{}'.format(t[0], t[1]), 'ds' + t[2], '|abc')

    def test_regression_punctuation_aliases_should_not_be_matched_as_mark_under_cursor(self):
        # There was a bug using aliases that caused alias characters to be
        # matched under the cursor e.g. `b` is aliased to `)` so feeding `ds)`
        # with content `(a|bc)` would result in `(a|c` because the `b` under the
        # cursor was matched as the begin part of `()`. This test prevents a
        # regression like that.
        for t in punctuation_targets_data:
            text = 'x{}|{}{}y'.format(t[0], t[2], t[1])
            expected = 'x|{}y'.format(t[2])
            self.eq(text, 'ds' + t[0], expected)  # Open
            self.eq(text, 'ds' + t[1], expected)  # Close
            self.eq(text, 'ds' + t[2], expected)  # Alias (close)

    def test_regression_ensure_dst_doesnt_match_the_t_under_the_cursor(self):
        self.eq('<i>|t</i>', 'dst', '|t')
        self.eq('<i>t|t</i>', 'dst', '|tt')
        self.eq('<t>t|t</t>', 'dst', '|tt')

    def test_punctuation_open_targets_should_search_multiline(self):
        expected = 'x |ab y'
        for t in punctuation_targets_data:
            self.eq('x {}\na|b{} y'.format(t[0], t[1]), 'ds' + t[0], expected)
            self.eq('x {}a|b\n{} y'.format(t[0], t[1]), 'ds' + t[0], expected)
            self.eq('x {}\na|b\n{} y'.format(t[0], t[1]), 'ds' + t[0], expected)
            self.eq('x {}\n\na|b{} y'.format(t[0], t[1]), 'ds' + t[0], expected)
            self.eq('x {}\n\n\na|b{} y'.format(t[0], t[1]), 'ds' + t[0], expected)

    def test_t_target_should_delete_tag(self):
        for t in tag_targets_data:
            self.eq('x {}a|b{} y'.format(t[0], t[1]), 'dst', 'x |ab y')

    def test_t_target_should_not_strip_contained_whitespace(self):
        for t in tag_targets_data:
            self.eq('x {}   a|b   {} y'.format(t[0], t[1]), 'dst', 'x |   ab    y')

    def test_t_target_should_not_delete_invalid_tags(self):
        for t in invalid_tag_targets_data:
            text = expected = 'x {}a|b{} y'.format(t[0], t[1])
            self.eq(text, 'dst', expected)


class TestIssues(unittest.FunctionalTestCase):

    def test_issue_305_multiple_selection_leaves_cursors_in_the_wrong_place(self):
        self.eq("eats 'fi|sh'\neats 'fi|sh'\neats 'fi|sh'", "ds'", "eats |fish\neats |fish\neats |fish")

    def test_issue_282(self):
        self.eq('|"Hello world!"', 'ds"', '|Hello world!')
        self.eq('"|Hello world!"', 'ds"', '|Hello world!')
        self.eq('"Hello |"world!"', 'ds"', '|Hello world!"')
        self.eq('"Hello "|world!"', 'ds"', '"Hello |world!')
        self.eq('"Hello\n|"world!"', 'ds"', '"Hello\n|world!')
        self.eq('"Hello\n"|world!"', 'ds"', '"Hello\n|world!')

    def test_issue_745(self):
        self.eq('hello |"fizz" world', 'ds"', 'hello |fizz world')
        self.eq('hello "fi|zz" world', 'ds"', 'hello |fizz world')
        self.eq('hello "fizz|" world', 'ds"', 'hello |fizz world')
        self.eq('he"ll\no |"fizz" world', 'ds"', 'he"ll\no |fizz world')
        self.eq('he(llo |(fizz) wo)rld', 'ds)', 'he(llo |fizz wo)rld')
        self.eq('he(llo (fizz|) wo)rld', 'ds)', 'he(llo |fizz wo)rld')

    def test_issue_644_nested_targets(self):
        self.eq(
            'return (kernel.std|out.readline().decode("utf-8").strip(),) x',
            'ds(',
            'return |kernel.stdout.readline().decode("utf-8").strip(), x')

        self.eq(
            'return (kernel.std|out.readline().decode("utf-8").strip(),) x',
            'ds)',
            'return |kernel.stdout.readline().decode("utf-8").strip(), x')

    def test_issue_744_nested_targets(self):
        self.eq(
            'document.addEventListener("mouseup", (fun|ction (_event) {\n    console.log("clicked!");\n}));',
            'ds(',
            'document.addEventListener("mouseup", |function (_event) {\n    console.log("clicked!");\n});')
        self.eq(
            'document.addEventListener("mouseup", (fun|ction (_event) {\n    console.log("clicked!");\n}));',
            'ds)',
            'document.addEventListener("mouseup", |function (_event) {\n    console.log("clicked!");\n});')
