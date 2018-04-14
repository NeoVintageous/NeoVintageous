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
from sublime import set_timeout
from sublime import load_settings


def ui_bell():
    # TODO Implement bell. See :h 'belloff'.
    # 'belloff' defaults to 'all' in Neovim.
    # See https://github.com/neovim/neovim/issues/2676.

    window = active_window()

    view = window.active_view()
    if not view:
        return

    # WIP feature toggle.
    enabled = view.settings().get('vintageous_wips', False)
    if not enabled:
        return

    belloff = view.settings().get('vintageous_belloff', 'all')
    if belloff == 'all':
        return

    # TODO How to make the bell theme adaptive i.e. work nice in light AND dark
    # color schemes.
    theme = 'Packages/NeoVintageous/res/Bell.tmTheme'

    duration = int(0.3 * 1000)

    if view.settings().get('vintageous_wips_bell_all_active_views', True):
        views = []
        for group in range(window.num_groups()):
            view = window.active_view_in_group(group)
            if view:
                settings = view.settings()
                settings.set('color_scheme', theme)
                views.append(view)

        def remove_bell():
            for view in views:
                view.settings().erase('color_scheme')

        set_timeout(remove_bell, duration)

    else:
        settings = view.settings()

        def remove_bell():
            settings.erase('color_scheme')

        settings.set('color_scheme', theme)
        set_timeout(remove_bell, duration)


# TODO [refactor] Rework this to use the ui_bell().
# TODO [refactor] Rework this to require a view or settings object.
def ui_blink(times=4, delay=55):
    prefs = load_settings('Preferences.sublime-settings')
    if prefs.get('vintageous_visualbell') is False:
        return

    view = active_window().active_view()
    if not view:
        return

    settings = view.settings()
    # Ensure we leave the setting as we found it.
    times = times if (times % 2) == 0 else times + 1

    def do_blink():
        nonlocal times
        if times > 0:
            settings.set('highlight_line', not settings.get('highlight_line'))
            times -= 1
            set_timeout(do_blink, delay)

    do_blink()


def ui_cmdline_prompt(window, initial_text, on_done, on_change, on_cancel):
    # type: (...) -> None
    input_panel = window.show_input_panel(
        '',
        initial_text,
        on_done,
        on_change,
        on_cancel
    )

    _set = input_panel.settings().set

    # Mark the input panel as a widget so we can later inspect that attribute
    # e.g. when hiding panels in _enter_normal_mode, and so that contexts such
    # as normal/visual/etc mode will ignore the widget.
    #
    # XXX This doesn't always work as expected, because the input panel is
    # already created before we setapply the settings, so there is a race-
    # condition.
    #
    # TODO [review] See if creating a Command-line mode.sublime-settings file
    # with all the relevant settings, including the "is_widget" setting solves
    # the race-condition issue described above.
    _set('is_widget', True)
    _set('is_vintageous_widget', True)

    _set('auto_complete', False)
    _set('auto_indent', False)
    _set('auto_match_enabled', False)
    _set('draw_centered', False)
    _set('draw_indent_guides', False)
    _set('gutter', False)
    _set('margin', 1)
    _set('match_selection', False)
    _set('rulers', [])
    _set('scroll_past_end', False)
    _set('smart_indent', False)
    _set('translate_tabs_to_spaces', False)
    _set('word_wrap', False)

    input_panel.assign_syntax(
        'Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
