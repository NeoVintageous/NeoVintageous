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

import sublime

if int(sublime.version()) < 4082:
    from Default.history_list import get_jump_history

    def jumplist_update(view) -> None:
        get_jump_history(view.window().id()).push_selection(view)

    def jumplist_back(view) -> tuple:
        return get_jump_history(view.window().id()).jump_back(view)

else:
    def jumplist_update(view) -> None:
        view.run_command("add_jump_record", {"selection": [(r.a, r.b) for r in view.sel()]})

    def jumplist_back(view) -> tuple:
        # No-op @see https://github.com/NeoVintageous/NeoVintageous/issues/806
        return (None, [])
