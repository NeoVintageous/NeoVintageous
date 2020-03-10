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

from sublime import Region
from sublime import version

from NeoVintageous.nv.jumplist import jumplist_update
from NeoVintageous.nv.ui import ui_bell
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import regions_transform_to_normal_mode
from NeoVintageous.nv.utils import regions_transformer
from NeoVintageous.nv.utils import resolve_visual_line_target
from NeoVintageous.nv.utils import resolve_visual_target
from NeoVintageous.nv.utils import set_selection
from NeoVintageous.nv.utils import show_if_not_visible
from NeoVintageous.nv.utils import wrapscan
from NeoVintageous.nv.vi.text_objects import find_next_lone_bracket
from NeoVintageous.nv.vi.text_objects import find_prev_lone_bracket
from NeoVintageous.nv.vim import EOF
from NeoVintageous.nv.vim import INTERNAL_NORMAL
from NeoVintageous.nv.vim import NORMAL
from NeoVintageous.nv.vim import VISUAL
from NeoVintageous.nv.vim import VISUAL_LINE
from NeoVintageous.nv.vim import enter_normal_mode
from NeoVintageous.nv.vim import status_message


def goto_help(window) -> None:
    view = window.active_view()
    if not view:
        raise ValueError('view is required')

    if not view.sel():
        raise ValueError('selection is required')

    sel = view.sel()[0]

    score = view.score_selector(sel.b, 'text.neovintageous jumptag')

    # TODO goto to help for any word in a help file. See :h bar Anyway, you can
    # use CTRL-] on any word, also when it is not within |, and Vim will try to
    # find help for it.  Especially for options in single quotes, e.g.
    # 'compatible'.

    if score == 0:
        return

    subject = view.substr(view.extract_scope(sel.b))
    if not subject:
        return

    if len(subject) > 50:
        return status_message('E149: Sorry, no help found')

    # TODO Refactor ex cmd internets to this common utility
    from NeoVintageous.nv.ex_cmds import do_ex_command
    do_ex_command(window, 'help', {'subject': subject})


def goto_line(view, mode: str, line_number: int) -> None:
    line_number = line_number if line_number > 0 else 1
    dest = view.text_point(line_number - 1, 0)

    def f(view, s):
        if mode == NORMAL:
            pt = next_non_blank(view, dest)
            if view.substr(pt) == EOF:
                pt = max(pt - 1, 0)

            return Region(pt)
        elif mode == INTERNAL_NORMAL:
            start_line = view.full_line(s.a)
            dest_line = view.full_line(dest)
            if start_line.a == dest_line.a:
                return dest_line
            elif start_line.a < dest_line.a:
                return Region(start_line.a, dest_line.b)
            else:
                return Region(start_line.b, dest_line.a)
        elif mode == VISUAL:
            dest_non_blank = next_non_blank(view, dest)
            if dest_non_blank < s.a and s.a < s.b:
                return Region(s.a + 1, dest_non_blank)
            elif dest_non_blank < s.a:
                return Region(s.a, dest_non_blank)
            elif dest_non_blank > s.b and s.a > s.b:
                return Region(s.a - 1, dest_non_blank + 1)
            return Region(s.a, dest_non_blank + 1)
        elif mode == VISUAL_LINE:
            if dest < s.a and s.a < s.b:
                return Region(view.full_line(s.a).b, dest)
            elif dest < s.a:
                return Region(s.a, dest)
            elif dest >= s.a and s.a > s.b:
                return Region(view.full_line(s.a - 1).a, view.full_line(dest).b)
            return Region(s.a, view.full_line(dest).b)
        return s

    jumplist_update(view)
    regions_transformer(view, f)
    jumplist_update(view)
    show_if_not_visible(view)


def _goto_modification(action: str, view, mode: str, count: int) -> None:
    with wrapscan(view, forward=(action == 'next')):
        if int(version()) >= 3189:
            for i in range(count):
                view.run_command(action + '_modification')

            a = view.sel()[0].a
            if view.substr(a) == '\n':
                if not view.line(a).empty():
                    a += 1

            set_selection(view, a)
            enter_normal_mode(view, mode)
        else:
            # TODO Remove DEPRECATED code, deprecated since build 3189
            view.run_command('git_gutter_' + action + '_change', {'count': count, 'wrap': False})
            line = view.line(view.sel()[0].b)
            if line.size() > 0:
                pt = view.find('^\\s*', line.begin()).end()
                if pt != line.begin():
                    set_selection(view, pt)


def goto_next_change(view, mode: str, count: int) -> None:
    _goto_modification('next', view, mode, count)


def goto_prev_change(view, mode: str, count: int) -> None:
    _goto_modification('prev', view, mode, count)


def goto_next_mispelled_word(view, mode: str, count: int) -> None:
    with wrapscan(view):
        for i in range(count):
            view.run_command('next_misspelling')

    regions_transform_to_normal_mode(view)


def goto_prev_mispelled_word(view, mode: str, count: int) -> None:
    with wrapscan(view, forward=False):
        for i in range(count):
            view.run_command('prev_misspelling')

    regions_transform_to_normal_mode(view)


def goto_prev_target(view, mode: str, count: int, target: str) -> None:
    targets = {
        '{': ('\\{', '\\}'),
        '(': ('\\(', '\\)'),
    }

    brackets = targets.get(target)
    if not brackets or mode not in (NORMAL, VISUAL, VISUAL_LINE):
        ui_bell()
        return

    def f(view, s):
        if mode == NORMAL:
            start = s.b
            if view.substr(start) == target:
                start -= 1

            prev_target = find_prev_lone_bracket(view, start, brackets)
            if prev_target is not None:
                return Region(prev_target.a)

        elif mode in (VISUAL, VISUAL_LINE):
            start = s.b
            if s.b > s.a:
                start -= 1

            if view.substr(start) == target:
                start -= 1

            prev_target = find_prev_lone_bracket(view, start, brackets)
            if prev_target:
                if mode == VISUAL:
                    resolve_visual_target(s, prev_target.a)
                elif mode == VISUAL_LINE:
                    resolve_visual_line_target(view, s, prev_target.a)

        return s

    regions_transformer(view, f)


def goto_next_target(view, mode: str, count: int, target: str) -> None:
    targets = {
        '}': ('\\{', '\\}'),
        ')': ('\\(', '\\)'),
    }

    brackets = targets.get(target)

    if not brackets or mode not in (NORMAL, VISUAL, VISUAL_LINE):
        ui_bell()
        return

    def f(view, s):
        if mode == NORMAL:
            start = s.b
            if view.substr(start) == target:
                start += 1

            bracket = find_next_lone_bracket(view, start, brackets, count)
            if bracket is not None:
                s = Region(bracket.a)

        elif mode in (VISUAL, VISUAL_LINE):
            start = s.b
            if s.b <= s.a and view.substr(start) == target:
                start += 1

            next_target = find_next_lone_bracket(view, start, brackets)
            if next_target:
                if mode == VISUAL:
                    resolve_visual_target(s, next_target.a)
                elif mode == VISUAL_LINE:
                    resolve_visual_line_target(view, s, next_target.a)

        return s

    regions_transformer(view, f)
