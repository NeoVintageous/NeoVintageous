from NeoVintageous.lib.vi.utils import mark_as_widget


def ui_cmdline_prompt(window, initial_text, on_done, on_change, on_cancel):
    input_panel = mark_as_widget(
        window.show_input_panel(
            '',
            initial_text,
            on_done,
            on_change,
            on_cancel))

    _set = input_panel.settings().set
    _set('auto_complete', False)
    _set('auto_indent', False)
    _set('auto_match_enabled', False)
    _set('draw_centered', False)
    _set('draw_indent_guides', False)
    _set('gutter', False)
    _set('is_widget', True)
    _set('margin', 1)
    _set('match_selection', False)
    _set('rulers', [])
    _set('scroll_past_end', False)
    _set('smart_indent', False)
    _set('translate_tabs_to_spaces', False)
    _set('word_wrap', False)

    input_panel.assign_syntax(
        'Packages/NeoVintageous/res/Command-line mode.sublime-syntax')
