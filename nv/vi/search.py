import re

from sublime import DRAW_NO_OUTLINE
from sublime import IGNORECASE
from sublime import LITERAL
from sublime import Region
import sublime_plugin


def find_in_range(view, term, start, end, flags=0):
    found = view.find(term, start, flags)
    if found and found.b <= end:
        return found


def find_all_in_range(view, term, start, end, flags=0):
    matches = []
    while True:
        m = find_in_range(view, term, start, end, flags)

        if m == Region(-1, -1):
            return matches

        if not m:
            return matches

        if m.end() > end or m.begin() < start:
            return matches

        matches.append(m)
        start = m.end()


def find_wrapping(view, term, start, end, flags=0, times=1):
    try:
        current_sel = view.sel()[0]
    except IndexError:
        return

    for x in range(times):
        match = find_in_range(view, term, start, end, flags)
        # make sure we wrap around the end of the buffer
        if not match:
            start = 0
            end = current_sel.a
            match = find_in_range(view, term, start, end, flags)
            if not match:
                return
        start = match.b

    return match


def reverse_find_wrapping(view, term, start, end, flags=0, times=1):
    current_sel = view.sel()[0]
    # Search wrapping around the end of the buffer.
    for x in range(times):
        match = reverse_search(view, term, start, end, flags)
        # Start searching in the lower half of the buffer if we aren't doing it yet.
        if not match and start <= current_sel.b:
            start = current_sel.b
            end = view.size()
            match = reverse_search(view, term, start, end, flags)
            if not match:
                return
        # No luck in the whole buffer.
        elif not match:
            return
        end = match.a

    return match


def find_last_in_range(view, term, start, end, flags=0):
    found = find_in_range(view, term, start, end, flags)
    last_found = found
    while found:
        found = find_in_range(view, term, found.b, end, flags)
        if not found or found.b > end:
            break
        last_found = found if found else last_found

    return last_found


# The @start position is linewise.
#
# The @end position is NOT linewise.
#
# For a characterwise reverse search use reverse_search_by_pt().
#
# TODO REVIEW The current implementation of the @end position is not technically
# not linewise. The start position *is* linewise. I don't know if this is
# causing bugs or if internals depends on this functionality, so "fixing it" and
# making it a true linewise search may break things in unexpected ways. It needs
# reviewing.
#
# The @start position is where the search ends.
#
# The @end position is where the search starts.
#
# TODO REVIEW The @end and @start position seem to be inverted i.e. the @start
# position should be the point where the search starts and the @end position
# should be where it ends oppose to the current behaviour.
#
# TODO should word the same as view.find() and return Region(-1, -1), rather than None, when not found
def reverse_search(view, term, start, end, flags=0):
    assert isinstance(start, int) or start is None
    assert isinstance(end, int) or end is None

    start = start if (start is not None) else 0
    end = end if (end is not None) else view.size()

    if start < 0 or end > view.size():
        return None

    lo_line = view.full_line(start)
    hi_line = view.full_line(end)

    while True:
        low_row, hi_row = view.rowcol(lo_line.a)[0], view.rowcol(hi_line.a)[0]
        middle_row = (low_row + hi_row) // 2

        middle_line = view.full_line(view.text_point(middle_row, 0))

        lo_region = Region(lo_line.a, middle_line.b)
        hi_region = Region(middle_line.b, min(hi_line.b, end))

        if find_in_range(view, term, hi_region.a, hi_region.b, flags):
            lo_line = view.full_line(middle_line.b)
        elif find_in_range(view, term, lo_region.a, lo_region.b, flags):
            hi_line = view.full_line(middle_line.a)
        else:
            return None

        if lo_line == hi_line:
            # we found the line we were looking for, now extract the match.
            return find_last_in_range(view, term, hi_line.a, min(hi_line.b, end), flags)


def reverse_search_by_pt(view, term, start, end, flags=0):
    assert isinstance(start, int) or start is None
    assert isinstance(end, int) or end is None

    start = start if (start is not None) else 0
    end = end if (end is not None) else view.size()

    if start < 0 or end > view.size():
        return None

    lo_line = view.full_line(start)
    hi_line = view.full_line(end)

    while True:
        low_row, hi_row = view.rowcol(lo_line.a)[0], view.rowcol(hi_line.a)[0]
        middle_row = (low_row + hi_row) // 2

        middle_line = view.full_line(view.text_point(middle_row, 0))

        lo_region = Region(lo_line.a, middle_line.b)
        hi_region = Region(middle_line.b, min(hi_line.b, end))

        if find_in_range(view, term, hi_region.a, hi_region.b, flags):
            lo_line = view.full_line(middle_line.b)
        elif find_in_range(view, term, lo_region.a, lo_region.b, flags):
            hi_line = view.full_line(middle_line.a)
        else:
            return None

        if lo_line == hi_line:
            # we found the line we were looking for, now extract the match.
            return find_last_in_range(view, term, max(hi_line.a, start), min(hi_line.b, end), flags)


# TODO [refactor] Move to commands module
class BufferSearchBase(sublime_plugin.TextCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_flags(self):
        # TODO: Implement smartcase?
        flags = 0
        if self.view.settings().get('vintageous_magic') is False:
            flags |= LITERAL

        if self.view.settings().get('vintageous_ignorecase') is True:
            flags |= IGNORECASE

        return flags

    def build_pattern(self, query):
        return query

    def hilite(self, query):
        regs = self.view.find_all(
            self.build_pattern(query),
            self.calculate_flags()
        )

        if not regs:
            self.view.erase_regions('vi_search')
            return

        # TODO: Re-enable hlsearch toggle setting.
        # if State(self.view).settings.vi['hlsearch'] == False:
        #     return

        self.view.add_regions('vi_search', regs, 'string.search.occurrence', '', DRAW_NO_OUTLINE)


# TODO [refactor] Move to commands module
class ExactWordBufferSearchBase(BufferSearchBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_flags(self):
        if self.view.settings().get('vintageous_ignorecase') is True:
            return IGNORECASE
        return 0

    def get_query(self):
        # TODO: make sure we swallow any leading white space.
        query = self.view.substr(self.view.word(self.view.sel()[0].end()))
        return query

    def build_pattern(self, query):
        return r'\b{0}\b'.format(re.escape(query))
