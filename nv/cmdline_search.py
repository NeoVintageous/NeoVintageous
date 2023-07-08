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

from NeoVintageous.nv.cmdline import Cmdline
from NeoVintageous.nv.history import history_update
from NeoVintageous.nv.history import reset_cmdline_history
from NeoVintageous.nv.search import add_search_highlighting
from NeoVintageous.nv.search import clear_search_highlighting
from NeoVintageous.nv.search import find_search_occurrences
from NeoVintageous.nv.search import process_search_pattern
from NeoVintageous.nv.settings import append_sequence
from NeoVintageous.nv.settings import get_count
from NeoVintageous.nv.settings import set_reset_during_init
from NeoVintageous.nv.state import evaluate_state
from NeoVintageous.nv.state import reset_command_data
from NeoVintageous.nv.state import set_motion
from NeoVintageous.nv.utils import get_insertion_point_at_b
from NeoVintageous.nv.utils import show_if_not_visible
from NeoVintageous.nv.vi.cmd_defs import ViSearchBackwardImpl
from NeoVintageous.nv.vi.cmd_defs import ViSearchForwardImpl
from NeoVintageous.nv.vi.search import find_wrapping
from NeoVintageous.nv.vi.search import reverse_find_wrapping
from NeoVintageous.nv.vim import status_message


class CmdlineSearch():

    def __init__(self, view, forward: bool):
        self.view = view
        self.forward = forward
        self.type = Cmdline.SEARCH_FORWARD if self.forward else Cmdline.SEARCH_BACKWARD

    def run(self, edit, pattern: str = '') -> None:
        set_reset_during_init(self.view, False)
        self._cmdline = Cmdline(
            self.view,
            self.type,
            self.on_done,
            self.on_change,
            self.on_cancel
        )

        self._cmdline.prompt(pattern)

    def on_done(self, pattern: str) -> None:
        history_update(self.type + pattern)
        reset_cmdline_history()
        clear_search_highlighting(self.view)
        append_sequence(self.view, pattern + '<CR>')
        if self.forward:
            set_motion(self.view, ViSearchForwardImpl(term=pattern))
        else:
            set_motion(self.view, ViSearchBackwardImpl(term=pattern))
        evaluate_state(self.view)

    def on_change(self, pattern: str) -> None:
        count = get_count(self.view)
        sel = self.view.sel()[0]
        pattern, flags = process_search_pattern(self.view, pattern)

        if self.forward:
            start = get_insertion_point_at_b(sel) + 1
            end = self.view.size()
        else:
            start = 0
            end = sel.b + 1 if not sel.empty() else sel.b

        if self.forward:
            match = find_wrapping(self.view,
                                  term=pattern,
                                  start=start,
                                  end=end,
                                  flags=flags,
                                  times=count)
        else:
            match = reverse_find_wrapping(self.view,
                                          term=pattern,
                                          start=start,
                                          end=end,
                                          flags=flags,
                                          times=count)

        clear_search_highlighting(self.view)

        if not match:
            return status_message('E486: Pattern not found: %s', pattern)

        add_search_highlighting(self.view, find_search_occurrences(self.view, pattern, flags), [match])
        show_if_not_visible(self.view, match)

    def on_cancel(self) -> None:
        clear_search_highlighting(self.view)
        reset_command_data(self.view)
        reset_cmdline_history()
        show_if_not_visible(self.view)
