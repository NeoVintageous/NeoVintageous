from contextlib import contextmanager

from sublime import Region
from sublime_plugin import TextCommand


# XXX The modes Use strings because we need to pass modes as arguments in
# Default.sublime-keymap and it's more readable.
COMMAND_LINE = 'mode_command_line'
CTRL_X = 'mode_control_x'
INSERT = 'mode_insert'
# NeoVintageous always runs actions based on selections. Some Vim commands,
# however, behave differently depending on whether the current mode is NORMAL or
# VISUAL. To differentiate NORMAL mode operations (involving only an action, or
# a motion plus an action) from VISUAL mode, we need to add an additional mode
# for handling selections that won't interfere with the actual VISUAL mode.
# This is INTERNAL_NORMAL's job. We consider INTERNAL_NORMAL a pseudomode,
# because global state's .mode property should never set to it, yet it's set in
# vi_cmd_data often.
# Note that for pure motions we still use plain NORMAL mode.
INTERNAL_NORMAL = 'mode_internal_normal'
NORMAL = 'mode_normal'
NORMAL_INSERT = 'mode_normal_insert'  # The mode you enter when giving i a count
OPERATOR_PENDING = 'mode_operator_pending'
REPLACE = 'mode_replace'
SELECT = 'mode_select'
UNKNOWN = 'mode_unknown'
VISUAL = 'mode_visual'
VISUAL_BLOCK = 'mode_visual_block'
VISUAL_LINE = 'mode_visual_line'


# TODO [refactor] I assume "INMEDIATE" is a typo, should be "IMMEDIATE"?
INPUT_INMEDIATE = 1
INPUT_VIA_PANEL = 2
INPUT_AFTER_MOTION = 3


DIRECTION_NONE = 0
DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4


def has_dirty_buffers(window):
    # type: (...) -> bool
    for v in window.views():
        if v.is_dirty():
            return True

    return False


def is_ignored(view):
    # type: (...) -> bool
    # Useful for external plugins to disable NeoVintageous for specific views.
    return view.settings().get('__vi_external_disable', False)


def is_ignored_but_command_mode(view):
    # type: (...) -> bool
    # Useful for external plugins to disable NeoVintageous for specific views.
    # Differs from is_ignored() in that only keys should be disabled.
    return view.settings().get('__vi_external_disable_keys', False)


def is_widget(view):
    # type: (...) -> bool
    get = view.settings().get

    return get('is_widget') or get('is_vintageous_widget')


def is_console(view):
    # type: (...) -> bool
    # TODO [review] Is this reliable?
    return (getattr(view, 'settings') is None)


def is_view(view):
    # type: (...) -> bool
    return not any((
        is_widget(view),
        is_console(view),
        is_ignored(view),
        is_ignored_but_command_mode(view)
    ))


def to_friendly_name(mode):
    # type: (int) -> str
    if mode == INSERT:
        return 'INSERT'
    if mode == INTERNAL_NORMAL:
        return ''
    if mode == NORMAL:
        return ''
    if mode == OPERATOR_PENDING:
        return ''
    if mode == VISUAL:
        return 'VISUAL'
    if mode == VISUAL_BLOCK:
        return 'VISUAL BLOCK'
    if mode == VISUAL_LINE:
        return 'VISUAL LINE'
    if mode == UNKNOWN:
        return 'UNKNOWN'
    if mode == REPLACE:
        return 'REPLACE'
    if mode == NORMAL_INSERT:
        return 'INSERT'
    if mode == SELECT:
        return 'SELECT'
    if mode == CTRL_X:
        return 'Mode ^X'

    return 'REALLY UNKNOWN'


def regions_transformer(view, f):
    # type: (...) -> None
    sels = list(view.sel())
    new = []
    for sel in sels:
        region = f(view, sel)
        if not isinstance(region, Region):
            raise TypeError('Region required')

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
    # type: (...) -> None
    # Apply f to every selection region in view and replace existing selections.
    sels = reversed(list(view.sel()))

    new_sels = []
    for s in sels:
        new_sels.append(f(view, s))

    view.sel().clear()
    for ns in new_sels:
        view.sel().add(ns)


def resolve_insertion_point_at_b(region):
    # type: (Region) -> int
    # Return the insertion point closest to region.b for a visual region.
    # For non-visual regions, the insertion point is always any of the region's
    # ends, so using this function is pointless.
    if region.a < region.b:
        return (region.b - 1)

    return region.b


def resolve_insertion_point_at_a(region):
    # type: (Region) -> int
    # Return the actual insertion point closest to region.a for a visual region.
    # For non-visual regions, the insertion point is always any of the region's
    # ends, so using this function is pointless.
    if region.size() == 0:
        raise TypeError('not a visual region')

    if region.a < region.b:
        return region.a
    elif region.b < region.a:
        return region.a - 1


# TODO REVIEW this function looks unused; it was refactored from an obsolete module
@contextmanager
def restoring_sels(view):
    old_sels = list(view.sel())
    yield
    view.sel().clear()
    for s in old_sels:
        # XXX: If the buffer has changed in the meantime, this won't work well.
        view.sel().add(s)


def new_inclusive_region(a, b):
    # type: (int, int) -> Region
    # Create a region that includes the char at a or b depending on new region's
    # orientation.
    if a <= b:
        return Region(a, b + 1)
    else:
        return Region(a + 1, b)


def row_at(view, pt):
    # type: (...) -> int
    return view.rowcol(pt)[0]


def col_at(view, pt):
    # type: (...) -> int
    return view.rowcol(pt)[1]


def row_to_pt(view, row, col=0):
    # type: (...) -> str
    return view.text_point(row, col)


@contextmanager
def gluing_undo_groups(view, state):
    state.processing_notation = True
    view.run_command('mark_undo_groups_for_gluing')
    yield
    view.run_command('glue_marked_undo_groups')
    state.processing_notation = False


class IrreversibleTextCommand(TextCommand):
    """Base class.

    The undo stack will ignore commands derived from this class. This is
    useful to prevent global state management commands from shadowing
    commands performing edits to the buffer, which are the important ones
    to keep in the undo history.
    """

    def __init__(self, view):
        TextCommand.__init__(self, view)

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
    # type: (...) -> int
    while (view.substr(pt) in white_space) and (pt <= view.size()):
        pt += 1

    return pt


def previous_non_white_space_char(view, pt, white_space='\t \n'):
    # type: (...) -> int
    while view.substr(pt) in white_space and pt > 0:
        pt -= 1

    return pt


# DEPRECATED
def previous_white_space_char(view, pt, white_space='\t '):
    # type: (...) -> int
    while pt >= 0 and view.substr(pt) not in white_space:
        pt -= 1

    return pt


def move_backward_while(view, pt, func):
    # type: (...) -> int
    while (pt >= 0) and func(pt):
        pt -= 1

    return pt


def is_at_eol(view, reg):
    # type: (...) -> bool
    return view.line(reg.b).b == reg.b


def is_at_bol(view, reg):
    # type: (...) -> bool
    return view.line(reg.b).a == reg.b


def first_row(view):
    # type: (...) -> int
    return view.rowcol(0)[0]


def last_row(view):
    # type: (...) -> int
    return view.rowcol(view.size())[0]


def translate_char(char):
    # type: (str) -> str
    lchar = char.lower()

    # FIXME What happens to keys like <home>, <up>, etc? We shouln't be
    # able to use those in some contexts, like as arguments to f, t...

    if lchar in ('<enter>', '<cr>'):
        return '\n'
    elif lchar in ('<sp>', '<space>'):
        return ' '
    elif lchar == '<lt>':
        return '<'
    elif lchar == '<tab>':
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
    # type: (...) -> Region
    return get_sel(view, -1)


def second_sel(view):
    # type: (...) -> Region
    return get_sel(view, 1)


def first_sel(view):
    # type: (...) -> Region
    return get_sel(view, 0)


def get_sel(view, i=0):
    # type: (...) -> Region
    return view.sel()[i]


def get_eol(view, pt, inclusive=False):
    # type: (...) -> int
    if not inclusive:
        return view.line(pt).end()

    return view.full_line(pt).end()


def get_bol(view, pt):
    # type: (...) -> int
    return view.line(pt).a


def replace_sel(view, new_sel):
    # type: (...) -> None
    if new_sel is None or new_sel == []:
        raise ValueError('no new_sel')

    view.sel().clear()
    if isinstance(new_sel, list):
        view.sel().add_all(new_sel)
        return

    view.sel().add(new_sel)


def resize_visual_region(r, b):
    # type: (Region, int) -> Region
    # Define a new visual mode region.
    #
    # Args:
    #   r (Region): Existing region.
    #   b (int): New end point.
    #
    # Returns:
    #   Region: Where x.a != x.b (XXX what does this mean?).
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
