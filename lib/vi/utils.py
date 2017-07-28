from contextlib import contextmanager

import sublime
from sublime import Region
import sublime_plugin

from NeoVintageous.lib import nvim


def mark_as_widget(view):
    """
    Mark @view as a widget so we can later inspect that attribute.

    For example, when hiding panels in _vi_enter_normal_mode.

    Used prominently by '/', '?' and ':'.

    XXX: This doesn't always work as we expect. For example, changing
         settings to a panel created instants before does not make those
         settings visible when the panel is activated. Investigate.
         We still need this so that contexts will ignore widgets, though.
         However, the fact that they are widgets should suffice to disable
         Vim keys for them...
    """
    view.settings().set('is_vintageous_widget', True)

    return view


def is_view(view):
    """
    Return `True` if @view is a normal view as NeoVintageous understands them.

    It returns `False` for views that have a `__vi_external_disable`
    setting set to `True`.
    """
    return not any((
        is_widget(view),
        is_console(view),
        is_ignored(view),
        is_ignored_but_command_mode(view)
    ))


def is_ignored(view):
    """
    Return `True` if the view wants to be ignored by NeoVintageous.

    Useful for external plugins that don't want NeoVintageous to be active for
    specific views.
    """
    return view.settings().get('__vi_external_disable', False)


def is_ignored_but_command_mode(view):
    """
    Return `True` if the view wants to be ignored by NeoVintageous.

    Useful for external plugins that don't want NeoVintageous to be active for
    specific views.

    .is_ignored_but_command_mode() differs from .is_ignored() in that here
    we declare that only keys should be disabled, not command mode.
    """
    return view.settings().get('__vi_external_disable_keys', False)


def is_widget(view):
    """Return `True` if the @view is any kind of widget."""
    setts = view.settings()

    return (setts.get('is_widget') or setts.get('is_vintageous_widget'))


def mark_as_widget(view):
    """
    Mark @view as a widget so we can later inspect that attribute.

    For example, when hiding panels in _vi_enter_normal_mode.

    Used prominently by '/', '?' and ':'.

    XXX: This doesn't always work as we expect. For example, changing
         settings to a panel created instants before does not make those
         settings visible when the panel is activated. Investigate.
         We still need this so that contexts will ignore widgets, though.
         However, the fact that they are widgets should suffice to disable
         Vim keys for them...
    """
    view.settings().set('is_vintageous_widget', True)

    return view


def is_console(view):
    """Return `True` if @view seems to be ST3's console."""
    # XXX: Is this reliable?
    return (getattr(view, 'settings') is None)


# Use strings because we need to pass modes as arguments in
# Default.sublime-keymap and it's more readable.
class modes:
    """Vim modes."""

    COMMAND_LINE = 'mode_command_line'
    INSERT = 'mode_insert'

    # NeoVintageous always runs actions based on selections. Some Vim commands,
    # however, behave differently depending on whether the current mode is NORMAL
    # or VISUAL. To differentiate NORMAL mode operations (involving only an
    # action, or a motion plus an action) from VISUAL mode, we need to add an
    # additional mode for handling selections that won't interfere with the actual
    # VISUAL mode.
    #
    # This is _MODE_INTERNAL_NORMAL's job. We consider _MODE_INTERNAL_NORMAL a
    # pseudomode, because global state's .mode property should never set to it,
    # yet it's set in vi_cmd_data often.
    #
    # Note that for pure motions we still use plain NORMAL mode.
    INTERNAL_NORMAL = 'mode_internal_normal'

    NORMAL = 'mode_normal'
    OPERATOR_PENDING = 'mode_operator_pending'
    VISUAL = 'mode_visual'
    VISUAL_BLOCK = 'mode_visual_block'
    VISUAL_LINE = 'mode_visual_line'
    UNKNOWN = 'mode_unknown'
    REPLACE = 'mode_replace'

    # The mode you enter when giving i a count
    NORMAL_INSERT = 'mode_normal_insert'

    SELECT = 'mode_select'
    CTRL_X = 'mode_control_x'

    @staticmethod
    def to_friendly_name(mode):
        # if name == COMMAND_LINE:
            # return 'INSERT'
        if mode == modes.INSERT:
            return 'INSERT'
        if mode == modes.INTERNAL_NORMAL:
            return ''
        if mode == modes.NORMAL:
            return ''
        if mode == modes.OPERATOR_PENDING:
            return ''
        if mode == modes.VISUAL:
            return 'VISUAL'
        if mode == modes.VISUAL_BLOCK:
            return 'VISUAL BLOCK'
        if mode == modes.VISUAL_LINE:
            return 'VISUAL LINE'
        if mode == modes.UNKNOWN:
            return 'UNKNOWN'
        if mode == modes.REPLACE:
            return 'REPLACE'
        if mode == modes.NORMAL_INSERT:
            return 'INSERT'
        if mode == modes.SELECT:
            return 'SELECT'
        if mode == modes.CTRL_X:
            return 'Mode ^X'
        else:
            return 'REALLY UNKNOWN'


class input_types:
    """Types of input parsers."""

    INMEDIATE = 1
    VIA_PANEL = 2
    AFTER_MOTION = 3


class jump_directions:
    FORWARD = 1
    BACK = 0


def regions_transformer(view, f):
    sels = list(view.sel())
    new = []
    for sel in sels:
        region = f(view, sel)
        if not isinstance(region, sublime.Region):
            raise TypeError('sublime.Region required')
        new.append(region)
    view.sel().clear()
    view.sel().add_all(new)


# TODO IMPORTANT was refactored from a module that removed vi/constants.py ...
#       but required by lib/cmds/actions.py module. This can
#       probably be refactored to use regions_transformer(), in
#       fact this function probably causes some bugs becayse
#       regions_transformer() is newer but this function was
#       looks like it was never updated.
def regions_transformer_reversed(view, f):
    """Apply @f to every selection region in ``view`` and replaces the existing selections."""
    sels = reversed(list(view.sel()))

    new_sels = []
    for s in sels:
        new_sels.append(f(view, s))

    view.sel().clear()
    for ns in new_sels:
        view.sel().add(ns)


def resolve_insertion_point_at_b(region):
    """
    Return the insertion point closest to @region.b for a visual region.

    For non-visual regions, the insertion point is always any of the region's
    ends, so using this function is pointless.

    @region
      A Sublime Text region.
    """
    if region.a < region.b:
        return (region.b - 1)

    return region.b


def resolve_insertion_point_at_a(region):
    """
    Return the actual insertion point closest to @region.a for a visual region.

    For non-visual regions, the insertion point is always any of the region's
    ends, so using this function is pointless.

    @region
      A Sublime Text region.
    """
    if region.size() == 0:
        raise TypeError('not a visual region')

    if region.a < region.b:
        return region.a
    elif region.b < region.a:
        return region.a - 1


def new_inclusive_region(a, b):
    """Create region that includes the char at @a or @b depending on new region's orientation."""
    if a <= b:
        return sublime.Region(a, b + 1)
    else:
        return sublime.Region(a + 1, b)


def row_at(view, pt):
    return view.rowcol(pt)[0]


def col_at(view, pt):
    return view.rowcol(pt)[1]


def row_to_pt(view, row, col=0):
    return view.text_point(row, col)


@contextmanager
def gluing_undo_groups(view, state):
    state.processing_notation = True
    view.run_command('mark_undo_groups_for_gluing')
    yield
    view.run_command('glue_marked_undo_groups')
    state.processing_notation = False


def blink(times=4, delay=55):
    prefs = sublime.load_settings('Preferences.sublime-settings')
    if prefs.get('vintageous_visualbell') is False:
        return

    v = sublime.active_window().active_view()
    settings = v.settings()
    # Ensure we leave the setting as we found it.
    times = times if (times % 2) == 0 else times + 1

    def do_blink():
        nonlocal times
        if times > 0:
            settings.set('highlight_line', not settings.get('highlight_line'))
            times -= 1
            sublime.set_timeout(do_blink, delay)

    do_blink()


class IrreversibleTextCommand(sublime_plugin.TextCommand):
    """Base class.

    The undo stack will ignore commands derived from this class. This is
    useful to prevent global state management commands from shadowing
    commands performing edits to the buffer, which are the important ones
    to keep in the undo history.
    """

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)

    def run_(self, edit_token, args):
        # We discard the edit_token because we don't want an IrreversibleTextCommand
        # to be added to the undo stack, but Sublime Text seems to still require
        # us to begin..end the token. If we removed those calls, the caret
        # would blink while motion keys were pressed, because --apparently--
        # we'd have an unclosed edit object around.
        args = self.filter_args(args)
        if args:
            edit = self.view.begin_edit(edit_token, self.name(), args)
            try:
                return self.run(**args)
            finally:
                self.view.end_edit(edit)
        else:
            edit = self.view.begin_edit(edit_token, self.name())
            try:
                return self.run()
            finally:
                self.view.end_edit(edit)

    def run(self, **kwargs):
        pass


def next_non_white_space_char(view, pt, white_space='\t '):
    while (view.substr(pt) in white_space) and (pt <= view.size()):
        pt += 1
    return pt


def previous_non_white_space_char(view, pt, white_space='\t \n'):
    while view.substr(pt) in white_space and pt > 0:
        pt -= 1
    return pt


# deprecated
def previous_white_space_char(view, pt, white_space='\t '):
    while pt >= 0 and view.substr(pt) not in white_space:
        pt -= 1
    return pt


def move_backward_while(view, pt, func):
    while (pt >= 0) and func(pt):
        pt -= 1
    return pt


def is_at_eol(view, reg):
    return view.line(reg.b).b == reg.b


def is_at_bol(view, reg):
    return view.line(reg.b).a == reg.b


def first_row(view):
    return view.rowcol(0)[0]


def last_row(view):
    return view.rowcol(view.size())[0]


def translate_char(char):
    # FIXME: What happens to keys like <home>, <up>, etc? We shouln't be
    #        able to use those in some contexts, like as arguments to f, t...
    if char.lower() in ('<enter>', '<cr>'):
        return '\n'
    elif char.lower() in ('<sp>', '<space>'):
        return ' '
    elif char.lower() == '<lt>':
        return '<'
    elif char.lower() == '<tab>':
        return '\t'
    else:
        return char


@contextmanager
def restoring_sel(view):
    regs = list(view.sel())
    view.sel().clear()
    yield
    view.sel().clear()
    view.sel().add_all(regs)


def last_sel(view):
    return get_sel(view, -1)


def second_sel(view):
    return get_sel(view, 1)


def first_sel(view):
    return get_sel(view, 0)


def get_sel(view, i=0):
    return view.sel()[i]


def get_eol(view, pt, inclusive=False):
    if not inclusive:
        return view.line(pt).end()
    return view.full_line(pt).end()


def get_bol(view, pt):
    return view.line(pt).a


def replace_sel(view, new_sel):
    if new_sel is None or new_sel == []:
        raise ValueError('no new_sel')
    view.sel().clear()
    if isinstance(new_sel, list):
        view.sel().add_all(new_sel)
        return
    view.sel().add(new_sel)


class directions:
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


def resize_visual_region(r, b):
    """
    Define a new visual mode region.

    Returns a region where x.a != x.b.

    @r
      Existing region.
    @b
      New end point.
    """
    if b < r.a:
        if r.b > r.a:
            return Region(r.a + 1, b)
        return Region(r.a, b)

    if b > r.a:
        if r.b < r.a:
            return Region(r.a - 1, b + 1)
        return Region(r.a, b + 1)

    return Region(b, b + 1)


@contextmanager
def adding_regions(view, name, regions, scope_name):
    view.add_regions(name, regions, scope_name)
    yield
    view.erase_regions(name)
