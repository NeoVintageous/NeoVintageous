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

from sublime import active_window
from sublime import DRAW_EMPTY_AS_OVERWRITE
from sublime import DRAW_NO_FILL
from sublime import DRAW_NO_OUTLINE
from sublime import DRAW_SOLID_UNDERLINE
from sublime import DRAW_SQUIGGLY_UNDERLINE
from sublime import DRAW_STIPPLED_UNDERLINE
from sublime import set_timeout

from NeoVintageous.nv.vim import status_message


def ui_bell(msg=None):
    if msg:
        status_message(msg)

    window = active_window()
    if not window:
        return

    view = window.active_view()
    if not view:
        return

    settings = view.settings()
    if settings.get('vintageous_belloff') == 'all':
        return

    color_scheme = settings.get('vintageous_bell_color_scheme', 'dark')
    if color_scheme in ('dark', 'light'):
        color_scheme = 'Packages/NeoVintageous/res/Bell-%s.hidden-color-scheme' % color_scheme

    duration = int(0.3 * 1000)
    times = 4
    delay = 55

    style = settings.get('vintageous_bell')

    if style == 'view':
        settings.set('color_scheme', color_scheme)

        def remove_bell():
            settings.erase('color_scheme')

        set_timeout(remove_bell, duration)
    elif style == 'views':
        views = []
        for group in range(window.num_groups()):
            view = window.active_view_in_group(group)
            if view:
                view.settings().set('color_scheme', color_scheme)
                views.append(view)

        def remove_bell():
            for view in views:
                view.settings().erase('color_scheme')

        set_timeout(remove_bell, duration)
    elif style == 'blink':
        # Ensure we leave the setting as we found it.
        times = times if (times % 2) == 0 else times + 1

        def do_blink():
            nonlocal times
            if times > 0:
                settings.set('highlight_line', not settings.get('highlight_line'))
                times -= 1
                set_timeout(do_blink, delay)

        do_blink()


_REGION_FLAGS = {
    'fill': DRAW_NO_OUTLINE,
    'outline': DRAW_NO_FILL,
    'squiggly_underline': DRAW_SQUIGGLY_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE | DRAW_EMPTY_AS_OVERWRITE,
    'stippled_underline': DRAW_STIPPLED_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE | DRAW_EMPTY_AS_OVERWRITE,
    'underline': DRAW_SOLID_UNDERLINE | DRAW_NO_FILL | DRAW_NO_OUTLINE | DRAW_EMPTY_AS_OVERWRITE,
}


def ui_region_flags(name):
    return _REGION_FLAGS.get(name)


def ui_highlight_yank(view):
    _get = view.settings().get

    if not _get('highlightedyank'):
        return

    view.add_regions(
        'highlightedyank',
        list(view.sel()),
        scope='string highlightedyank',
        flags=ui_region_flags(_get('highlightedyank_style'))
    )

    set_timeout(
        lambda: view.erase_regions('highlightedyank'),
        _get('highlightedyank_duration')
    )


def ui_highlight_yank_clear(view):
    view.erase_regions('highlightedyank')
