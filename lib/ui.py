

def ui_cmdline_prompt(window, initial_text, on_done, on_change, on_cancel):
    # type: (...) -> None
    input_panel = window.show_input_panel(
        '',
        initial_text,
        on_done,
        on_change,
        on_cancel)

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
