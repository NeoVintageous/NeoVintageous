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

import re

from sublime import active_window

from NeoVintageous.nv.ex_cmds import do_ex_cmdline
from NeoVintageous.nv.options import get_option
from NeoVintageous.nv.vim import message


_MODELINE_PATTERN = re.compile(
    '(^|\\s+)'
    '([vV]im?|ex):\\s*'
    '(?:(set)\\s+([^:]+):|(.+))')


def _parse_line(line: str):
    matches = _MODELINE_PATTERN.search(line)
    if not matches:
        return

    leading_ws = matches.group(1)
    key = matches.group(2)

    # The white space before {vi:|vim:|Vim:|ex:} is required.  This minimizes
    # the chance that a normal word like "lex:" is caught.  There is one
    # exception: "vi:" and "vim:" can also be at the start of the line (for
    # compatibility with version 3.0).  Using "ex:" at the start of the line
    # will be ignored (this could be short for "example:").
    if not leading_ws and key not in ('vim', 'vi'):
        return

    # 1st form examples:
    #    vi:noai:sw=3 ts=6
    #    vim: tw=77
    # 2nd form xamples:
    #    /* vim: set ai tw=75: */
    #    /* Vim: set ai tw=75: */
    # See :help modeline
    is_1st_form = not matches.group(3)

    if is_1st_form:
        return re.split('[: ]', matches.group(5).rstrip(':'))
    else:
        return matches.group(4).strip().split(' ')


def do_modeline(view) -> None:
    # A feature similar to vim modeline. A number of lines at the beginning and
    # end of the file are checked for modelines. The number of lines checked is
    # controlled by the 'modelines' option, the default is 5.
    #
    # Examples:
    #   vim: number
    #   vim: nonumber
    #   vim: tabstop=4
    #   vim: ts=4 noet
    window = view.window()

    # If the view is "transient" (for example when opened in in preview via the
    # CTRL-p overlay) then the view won't have a window object. Some ST events
    # like on_load() may open transient views.
    if not window:
        window = active_window()

    if window:
        modelines = get_option(view, 'modelines')
        line_count = view.rowcol(view.size())[0] + 1
        head_lines = range(0, min(modelines, line_count))
        tail_lines = range(max(0, line_count - modelines), line_count)
        lines = list(set(list(head_lines) + list(tail_lines)))

        for i in lines:
            line = view.line(view.text_point(i, 0))
            if line.size() > 0:
                options = _parse_line(view.substr(line))
                if options:
                    for option in options:
                        if option.strip().startswith('shell'):
                            message('Error detected while processing modelines:')
                            message('line %s:', str(i + 1))
                            message('E520: Not allowed in a modeline: %s', option)
                        else:
                            do_ex_cmdline(window, ':setlocal ' + option)
