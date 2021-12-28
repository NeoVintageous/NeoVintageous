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

from sublime import CLASS_EMPTY_LINE
from sublime import CLASS_LINE_END
from sublime import CLASS_LINE_START
from sublime import CLASS_PUNCTUATION_END
from sublime import CLASS_PUNCTUATION_START
from sublime import CLASS_WORD_END
from sublime import CLASS_WORD_START
from sublime import IGNORECASE
from sublime import Region

from NeoVintageous.nv.polyfill import re_escape
from NeoVintageous.nv.polyfill import view_find
from NeoVintageous.nv.polyfill import view_find_in_range
from NeoVintageous.nv.polyfill import view_indentation_level
from NeoVintageous.nv.polyfill import view_indented_region
from NeoVintageous.nv.polyfill import view_rfind_all
from NeoVintageous.nv.utils import get_insertion_point_at_b
from NeoVintageous.nv.utils import next_non_blank
from NeoVintageous.nv.utils import next_non_ws
from NeoVintageous.nv.utils import prev_non_blank
from NeoVintageous.nv.utils import prev_non_ws
from NeoVintageous.nv.vi.search import find_in_range
from NeoVintageous.nv.vi.search import reverse_search_by_pt
from NeoVintageous.nv.vi.units import word_starts


RX_ANY_TAG = r'</?([0-9A-Za-z-]+).*?>'
RX_ANY_TAG_NAMED_TPL = r'</?({0}) *?.*?>'
RXC_ANY_TAG = re.compile(r'</?([0-9A-Za-z]+).*?>')
# According to the HTML 5 editor's draft, only 0-9A-Za-z characters can be
# used in tag names. TODO: This won't be enough in Dart Polymer projects,
# for example.
RX_ANY_START_TAG = r'<([0-9A-Za-z]+)(.*?)>'
RX_ANY_END_TAG = r'</([0-9A-Za-z-]+).*?>'


ANCHOR_NEXT_WORD_BOUNDARY = CLASS_WORD_START | CLASS_PUNCTUATION_START | CLASS_LINE_END
ANCHOR_PREVIOUS_WORD_BOUNDARY = CLASS_WORD_END | CLASS_PUNCTUATION_END | CLASS_LINE_START

WORD_REVERSE_STOPS = CLASS_WORD_START | CLASS_EMPTY_LINE | CLASS_PUNCTUATION_START
WORD_END_REVERSE_STOPS = CLASS_WORD_END | CLASS_EMPTY_LINE | CLASS_PUNCTUATION_END


BRACKET = 1
QUOTE = 2
SENTENCE = 3
TAG = 4
WORD = 5
BIG_WORD = 6
PARAGRAPH = 7
INDENT = 8
BIG_INDENT = 9
LINE = 10


PAIRS = {
    '"': (('"', '"'), QUOTE),
    "'": (("'", "'"), QUOTE),
    '`': (('`', '`'), QUOTE),
    '#': (('#', '#'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '$': (('$', '$'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '&': (('&', '&'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '*': (('*', '*'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '+': (('+', '+'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    ',': ((',', ','), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '-': (('-', '-'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '.': (('.', '.'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '/': (('/', '/'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    ':': ((':', ':'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    ';': ((';', ';'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '=': (('=', '='), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '_': (('_', '_'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '|': (('|', '|'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '~': (('~', '~'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '\\': (('\\', '\\'), QUOTE),  # {plugin https://github.com/wellle/targets.vim}
    '(': (('\\(', '\\)'), BRACKET),
    ')': (('\\(', '\\)'), BRACKET),
    '[': (('\\[', '\\]'), BRACKET),
    ']': (('\\[', '\\]'), BRACKET),
    '{': (('\\{', '\\}'), BRACKET),
    '}': (('\\{', '\\}'), BRACKET),
    '<': (('<', '>'), BRACKET),
    '>': (('<', '>'), BRACKET),
    'b': (('\\(', '\\)'), BRACKET),
    'B': (('\\{', '\\}'), BRACKET),
    'p': (None, PARAGRAPH),
    's': (None, SENTENCE),
    't': (None, TAG),
    'W': (None, BIG_WORD),
    'w': (None, WORD),
    'I': (None, BIG_INDENT),  # {not in Vim}
    'i': (None, INDENT),  # {not in Vim}
    'l': (None, LINE),
}  # type: dict


def is_at_punctuation(view, pt: int) -> bool:
    char = view.substr(pt)
    # FIXME Wrong if pt is at '\t'
    return (not (is_at_word(view, pt) or char.isspace() or char == '\n') and char.isprintable())


def is_at_word(view, pt: int) -> bool:
    char = view.substr(pt)

    return char.isalnum() or char == '_'


def is_at_space(view, pt: int) -> bool:
    return view.substr(pt).isspace()


def get_punctuation_region(view, pt: int) -> Region:
    start = view.find_by_class(pt + 1, forward=False, classes=CLASS_PUNCTUATION_START)
    end = view.find_by_class(pt, forward=True, classes=CLASS_PUNCTUATION_END)

    return Region(start, end)


def get_space_region(view, pt: int) -> Region:
    end = view.find_by_class(pt, forward=True, classes=ANCHOR_NEXT_WORD_BOUNDARY)

    return Region(previous_word_end(view, pt + 1), end)


def previous_word_end(view, pt: int) -> int:
    return view.find_by_class(pt, forward=False, classes=ANCHOR_PREVIOUS_WORD_BOUNDARY)


def next_word_start(view, pt: int) -> int:
    if is_at_punctuation(view, pt):
        # Skip all punctuation surrounding the caret and any trailing spaces.
        end = get_punctuation_region(view, pt).b
        if view.substr(end) in (' ', '\n'):
            end = view.find_by_class(end, forward=True, classes=ANCHOR_NEXT_WORD_BOUNDARY)

            return end

    elif is_at_space(view, pt):
        # Skip all spaces surrounding the cursor and the text word.
        end = get_space_region(view, pt).b
        if is_at_word(view, end) or is_at_punctuation(view, end):
            end = view.find_by_class(
                end,
                forward=True,
                classes=CLASS_WORD_END | CLASS_PUNCTUATION_END | CLASS_LINE_END
            )

            return end

    # Skip the word under the caret and any trailing spaces.
    return view.find_by_class(pt, forward=True, classes=ANCHOR_NEXT_WORD_BOUNDARY)


def current_word_start(view, pt: int) -> int:
    if is_at_punctuation(view, pt):
        return get_punctuation_region(view, pt).a
    elif is_at_space(view, pt):
        return get_space_region(view, pt).a

    return view.word(pt).a


def current_word_end(view, pt: int) -> int:
    if is_at_punctuation(view, pt):
        return get_punctuation_region(view, pt).b
    elif is_at_space(view, pt):
        return get_space_region(view, pt).b

    return view.word(pt).b


# https://vimhelp.appspot.com/motion.txt.html#word
# Used for motions in operations like daw and caw
def _a_word(view, pt: int, inclusive: bool = True, count: int = 1) -> Region:
    start = current_word_start(view, pt)
    end = pt

    if inclusive:
        end = word_starts(view, start, count=count, internal=True)

        # If there is no space at the end of our word text object, include any
        # preceding spaces. (Follows Vim behavior.)
        if (not view.substr(end - 1).isspace() and view.substr(start - 1).isspace()):
            start = prev_non_blank(view, start - 1) + 1

        # Vim does some inconsistent stuff here...
        if count > 1 and view.substr(end) == '\n':
            end += 1

        return Region(start, end)

    for x in range(count):
        end = current_word_end(view, end)

    return Region(start, end)


def big_word_end(view, pt: int) -> int:
    prev = pt
    while True:
        if is_at_punctuation(view, pt):
            pt = get_punctuation_region(view, pt).b
        elif is_at_word(view, pt):
            pt = current_word_end(view, pt)
        else:
            break

        if pt == prev:
            # Guards against run-away loops
            break

        prev = pt

    return pt


def big_word_start(view, pt: int) -> int:
    prev = pt
    while True:
        if is_at_punctuation(view, pt):
            pt = get_punctuation_region(view, pt).a - 1
        elif is_at_word(view, pt):
            pt = current_word_start(view, pt) - 1
        else:
            break

        if pt == prev:
            # Guards against run-away loops
            break

        prev = pt

    return pt + 1


# https://vimhelp.appspot.com/motion.txt.html#WORD
# Used for motions in operations like daW and caW
def a_big_word(view, pt: int, inclusive: bool = False, count: int = 1) -> Region:
    start, end = None, pt
    for x in range(count):
        if is_at_space(view, end):
            if start is None:
                start = get_space_region(view, pt).a

            if inclusive:
                end = big_word_end(view, get_space_region(view, end).b)
            else:
                end = get_space_region(view, end).b

        if is_at_punctuation(view, end):
            if start is None:
                start = big_word_start(view, end)

            end = big_word_end(view, end)

            if inclusive and is_at_space(view, end):
                end = get_space_region(view, end).b

        else:
            if start is None:
                start = big_word_start(view, end)

            end = big_word_end(view, end)

            if inclusive and is_at_space(view, end):
                end = get_space_region(view, end).b

    if start is None:
        return Region(end)

    return Region(start, end)


def _get_text_object_tag(view, s: Region, inclusive: bool, count: int) -> Region:
    # When the active cursor position is on leading whitespace before a tag on
    # the same line then the start point of the text object is the tag.
    line = view.line(get_insertion_point_at_b(s))
    tag_in_line = view_find_in_range(view, '^\\s*<[^>]+>', line.begin(), line.end())
    if tag_in_line:
        if s.b >= s.a and s.b < tag_in_line.end():
            if s.empty():
                s.a = s.b = tag_in_line.end()
            else:
                s.a = tag_in_line.end()
                s.b = tag_in_line.end() + 1

    begin_tag, end_tag, _ = find_containing_tag(view, s.begin())
    if not (begin_tag and end_tag):
        return s

    # The normal method is to select a <tag> until the matching </tag>. For "at"
    # the tags are included, for "it" they are excluded. But when "it" is
    # repeated the tags will be included (otherwise nothing would change).
    if not inclusive:
        if s and s == Region(begin_tag.end(), end_tag.begin()):
            inclusive = True

    if inclusive:
        return Region(begin_tag.a, end_tag.b)
    else:
        return Region(begin_tag.b, end_tag.a)


def _get_text_object_paragraph(view, s: Region, inclusive: bool, count: int) -> Region:
    return find_paragraph_text_object(view, s, inclusive, count)


def _get_text_object_bracket(view, s: Region, inclusive: bool, count: int, delims: tuple) -> Region:
    opening = find_prev_lone_bracket(view, max(0, s.begin()), delims)
    closing = find_next_lone_bracket(view, s.end(), delims)

    if not (opening and closing):
        return s

    if inclusive:
        return Region(opening.a, closing.b)

    a = opening.a + 1
    if view.substr(a) == '\n':
        a += 1

    b = closing.b - 1

    if b > a:
        line = view.line(b)

        if next_non_blank(view, line.a) + 1 == line.b:
            row_a, col_a = view.rowcol(a - 1)
            row_b, col_b = view.rowcol(b + 1)
            if (row_b - 1) > row_a:
                line = view.full_line(view.text_point((row_b - 1), 0))

                return Region(a, line.b)

    return Region(a, b)


def _get_text_object_quote(view, s: Region, inclusive: bool, count: int, delims: tuple) -> Region:
    line = view.line(s)

    delim_open = delims[0]
    delim_open = re_escape(delim_open)

    # FIXME: Escape sequences like \" are probably syntax-dependant.
    prev_quote = reverse_search_by_pt(view, r'(?<!\\\\)' + delim_open, start=line.a, end=s.b)
    next_quote = find_in_range(view, r'(?<!\\\\)' + delim_open, start=s.b, end=line.b)

    if next_quote and not prev_quote:
        prev_quote = next_quote
        next_quote = find_in_range(view, r'(?<!\\\\)' + delim_open, start=prev_quote.b, end=line.b)

    if not (prev_quote and next_quote):
        return s

    if inclusive:
        return Region(prev_quote.a, next_quote.b)

    return Region(prev_quote.a + 1, next_quote.b - 1)


def _get_text_object_word(view, s: Region, inclusive: bool, count: int) -> Region:
    if s.size() == 1:
        pt = get_insertion_point_at_b(s)
    else:
        if s.b < s.a:
            pt = max(0, s.b - 1)
        else:
            pt = s.b

    w = _a_word(view, pt, inclusive=inclusive, count=count)
    if s.size() <= 1:
        return w

    if s.b >= s.a:
        return Region(s.a, w.b)
    else:
        return Region(s.a, w.a)

    return s


def _get_text_object_big_word(view, s: Region, inclusive: bool, count: int) -> Region:
    w = a_big_word(view, s.b, inclusive=inclusive, count=count)
    if s.size() <= 1:
        return w

    return Region(s.a, w.b)


def _get_text_object_sentence(view, s: Region, inclusive: bool, count: int) -> Region:
    sentence_start = view.find_by_class(s.b, forward=False, classes=CLASS_EMPTY_LINE)
    sentence_start_2 = reverse_search_by_pt(view, r'[.?!:]\s+|[.?!:]$', start=0, end=s.b)
    if sentence_start_2:
        sentence_start = (sentence_start + 1 if (sentence_start > sentence_start_2.b) else sentence_start_2.b)
    else:
        sentence_start = sentence_start + 1

    sentence_end = find_in_range(view, r'([.?!:)](?=\s))|([.?!:)]$)', start=s.b, end=view.size())
    if not sentence_end:
        return s

    if inclusive:
        return Region(sentence_start, sentence_end.b)
    else:
        return Region(sentence_start, sentence_end.b)


def _get_text_object_line(view, s: Region, inclusive: bool, count: int) -> Region:
    start, end = find_line_text_object(view, s)

    return Region(start, end)


def get_text_object_region(view, s: Region, text_object: str, inclusive: bool = False, count: int = 1) -> Region:
    try:
        delims, type_ = PAIRS[text_object]
    except KeyError:
        return s

    if type_ == TAG:
        return _get_text_object_tag(view, s, inclusive, count)
    elif type_ == PARAGRAPH:
        return _get_text_object_paragraph(view, s, inclusive, count)
    elif type_ == BRACKET:
        return _get_text_object_bracket(view, s, inclusive, count, delims)
    elif type_ == QUOTE:
        return _get_text_object_quote(view, s, inclusive, count, delims)
    elif type_ == WORD:
        return _get_text_object_word(view, s, inclusive, count)
    elif type_ == BIG_WORD:
        return _get_text_object_big_word(view, s, inclusive, count)
    elif type_ == SENTENCE:
        return _get_text_object_sentence(view, s, inclusive, count)
    elif type_ == LINE:
        return _get_text_object_line(view, s, inclusive, count)
    elif type_ in (INDENT, BIG_INDENT):
        # A port of https://github.com/michaeljsmith/vim-indent-object. {not in Vim}
        resolve_indent_text_object(view, s, inclusive, big=(type_ == BIG_INDENT))

    return s


def find_next_lone_bracket(view, start: int, items, unbalanced: int = 0):
    # TODO: Extract common functionality from here and the % motion instead of
    # duplicating code.
    new_start = start
    for i in range(unbalanced or 1):
        next_closing_bracket = find_in_range(
            view,
            items[1],
            start=new_start,
            end=view.size(),
            flags=IGNORECASE
        )

        if next_closing_bracket is None:
            # Unbalanced items; nothing we can do.
            return

        while view.substr(next_closing_bracket.begin() - 1) == '\\':
            next_closing_bracket = find_in_range(view, items[1],
                                                 start=next_closing_bracket.end(),
                                                 end=view.size(),
                                                 flags=IGNORECASE)
            if next_closing_bracket is None:
                return

        new_start = next_closing_bracket.end()

    if view.substr(start) == items[0][-1]:
        start += 1

    nested = 0
    while True:
        next_opening_bracket = find_in_range(view, items[0],
                                             start=start,
                                             end=next_closing_bracket.b,
                                             flags=IGNORECASE)
        if not next_opening_bracket:
            break

        nested += 1
        start = next_opening_bracket.end()

    if nested > 0:
        return find_next_lone_bracket(view, next_closing_bracket.end(),
                                      items,
                                      nested)
    else:
        return next_closing_bracket


def find_prev_lone_bracket(view, start: int, tags, unbalanced: int = 0):
    # TODO: Extract common functionality from here and the % motion instead of
    # duplicating code.

    # XXX: refactor this
    if view.substr(start) == (tags[0][1] if len(tags[0]) > 1 else tags[0]):
        if not unbalanced and view.substr(start - 1) != '\\':
            return Region(start, start + 1)

    new_start = start
    for i in range(unbalanced or 1):
        prev_opening_bracket = reverse_search_by_pt(view, tags[0],
                                                    start=0,
                                                    end=new_start,
                                                    flags=IGNORECASE)

        if prev_opening_bracket is None:
            # Unbalanced tags; nothing we can do.
            return

        while view.substr(prev_opening_bracket.begin() - 1) == '\\':
            prev_opening_bracket = reverse_search_by_pt(
                view,
                tags[0],
                start=0,
                end=prev_opening_bracket.begin(),
                flags=IGNORECASE
            )

            if prev_opening_bracket is None:
                return

        new_start = prev_opening_bracket.begin()

    nested = 0
    while True:
        next_closing_bracket = reverse_search_by_pt(view,
                                                    tags[1],
                                                    start=prev_opening_bracket.a,
                                                    end=start,
                                                    flags=IGNORECASE)
        if not next_closing_bracket:
            break

        nested += 1
        start = next_closing_bracket.begin()

    if nested > 0:
        return find_prev_lone_bracket(view,
                                      prev_opening_bracket.begin(),
                                      tags,
                                      nested)
    else:
        return prev_opening_bracket


def find_paragraph_text_object(view, s: Region, inclusive: bool = True, count: int = 1) -> Region:
    # In Vim, `vip` will select an inner paragraph -- all the lines having the
    # same whitespace status of the current location. And a `vap` will select
    # both the current inner paragraph (either whitespace or not) and the next
    # inner paragraph (the opposite).
    begin = None
    end = s.a
    for _ in range(count):
        b1, e1 = find_inner_paragraph(view, end)
        b2, end = find_inner_paragraph(view, e1) if inclusive else (b1, e1)
        if begin is None:
            begin = b1

    if begin is None:
        return Region(end)

    return Region(begin, end)


def find_sentences_forward(view, start, count: int = 1):
    def _find_sentence_forward(view, start: int):
        char = view.substr(start)
        if char == '\n':
            next_sentence = view.find('\\s+', start)
        else:
            next_sentence = view.find('[\\.\\?\\!][\\)\\]"\']*\\s', start)

        if next_sentence:
            return next_non_blank(view, next_sentence.b)

    start = start.b if isinstance(start, Region) else start

    new_start = start
    for i in range(count):
        next_sentence = _find_sentence_forward(view, new_start)
        if not next_sentence:
            break

        new_start = next_sentence

    if new_start != start:
        return Region(new_start)


def find_sentences_backward(view, start_pt: int, count: int = 1) -> Region:
    if isinstance(start_pt, Region):
        start_pt = start_pt.a

    pt = prev_non_ws(view, start_pt)
    sen = Region(pt)
    prev = sen
    while True:
        sen = view.expand_by_class(sen, CLASS_LINE_END | CLASS_PUNCTUATION_END)
        if sen.a <= 0 or view.substr(sen.begin() - 1) in ('.', '\n', '?', '!'):
            if view.substr(sen.begin() - 1) == '.' and not view.substr(sen.begin()) == ' ':
                continue

            if prev == sen:
                break

            prev = sen

            if sen:
                pt = next_non_blank(view, sen.a)
                if pt < sen.b and pt != start_pt:
                    if view.substr(pt) == '\n':
                        if pt + 1 != start_pt:
                            pt += 1

                    return Region(pt)

                if pt > 0:
                    continue

            return sen

    return sen


def find_inner_paragraph(view, initial_loc):
    """
    Take a location, as an integer.

    Returns a (begin, end) tuple of ints for the Vim inner paragraph
    corresponding to that location. An inner paragraph consists of a set of
    contiguous lines all having the same whitespace status (a line either
    consists entirely of whitespace characters or it does not).
    """
    # Determine whether the initial point lies in an all-whitespace line.
    def is_whitespace(region):
        return len(view.substr(region).strip()) == 0

    iws = is_whitespace(view.line(initial_loc))

    # Search backward finding all lines with similar whitespace status.
    # This will give use the value for begin.
    p = initial_loc
    while True:
        line = view.line(p)
        if is_whitespace(line) != iws:
            break
        elif line.begin() == 0:
            p = 0
            break

        p = line.begin() - 1

    begin = p + 1 if p > 0 else p

    # To get the value for end, we do the same thing, this time searching forward.
    p = initial_loc
    while True:
        line = view.line(p)
        if is_whitespace(line) != iws:
            break

        p = line.end() + 1

        if p >= view.size():
            break

    end = p

    return (begin, end)


def resolve_indent_text_object(view, s: Region, inclusive: bool = True, big: bool = False):
    # Look for the minimum indentation in the current visual region.
    idnt = 1000
    idnt_pt = None
    for line in view.lines(s):
        if not re.match('^\\s*$', view.substr(line)):
            level = view.indentation_level(line.a)
            if level < idnt:
                idnt = min(idnt, level)
                idnt_pt = line.a

    # If the selection has no indentation at all, find which indentation level
    # is the largest, the previous non blank before tphe cursor or the next non
    # blank after the cursor, and start the selection from that point.

    if idnt == 1000:
        pnb_pt = prev_non_ws(view, s.begin())
        pnb_indent_level = view_indentation_level(view, pnb_pt)

        nnb_pt = next_non_ws(view, s.end())
        nnb_indent_level = view_indentation_level(view, nnb_pt)

        if pnb_indent_level > nnb_indent_level:
            idnt_pt = s.a = s.b = pnb_pt
        elif nnb_indent_level > pnb_indent_level:
            idnt_pt = s.a = s.b = nnb_pt
        else:
            idnt_pt = pnb_pt

    if idnt == 0 and idnt_pt is not None:
        expanded = view.expand_by_class(s, CLASS_EMPTY_LINE)
        s.a = expanded.a
        s.b = expanded.b

        if not inclusive:
            # Case: ii and iI. Strip any leading whitespace.
            leading_ws = view_find(view, '\\s*', s.a)
            if leading_ws is not None:
                s.a = view.line(leading_ws.b).a

            s.b = prev_non_blank(view, s.b)
        elif big:
            # Case: aI. Add a line below.
            if view.substr(s.b) == '\n':
                s.b += 1

    elif idnt > 0 and idnt_pt is not None:
        indented_region = view_indented_region(view, idnt_pt, inclusive)

        if indented_region.begin() < s.begin():
            s.a = indented_region.begin()

        if indented_region.end() > s.end():
            s.b = indented_region.end()

        if inclusive:
            # Case: ai. Add a line above.
            s.a = view.line(view.text_point(view.rowcol(s.a)[0] - 1, 0)).a

            # Case: aI. Add a line below.
            if big:
                s.b = view.full_line(view.text_point(view.rowcol(s.b - 1)[0] + 1, 0)).b

    return s


def find_line_text_object(view, s: Region) -> tuple:
    line = view.line(s)
    line_content = view.substr(line)

    begin = line.begin()
    end = line.end()

    whitespace_match = re.match("\\s+", line_content)
    if whitespace_match:
        begin = begin + len(whitespace_match.group(0))

    return (begin, end)


# TODO: Move this to units.py.
def word_reverse(view, pt: int, count: int = 1, big: bool = False) -> int:
    t = pt
    for _ in range(count):
        t = view.find_by_class(t, forward=False, classes=WORD_REVERSE_STOPS)
        if t == 0:
            break

        if big:
            # Skip over punctuation characters.
            while not ((view.substr(t - 1) in '\n\t ') or (t <= 0)):
                t -= 1

    return t


# TODO: Move this to units.py.
def big_word_reverse(view, pt: int, count: int = 1) -> int:
    return word_reverse(view, pt, count, big=True)


# TODO: Move this to units.py.
def word_end_reverse(view, pt: int, count: int = 1, big: bool = False) -> int:
    t = pt
    for i in range(count):
        if big:
            # Skip over punctuation characters.
            while not ((view.substr(t - 1) in '\n\t ') or (t <= 0)):
                t -= 1

        # `ge` should stop at the previous word end if starting at a space
        # immediately after a word.
        if (i == 0 and view.substr(t).isspace() and not view.substr(t - 1).isspace()):
            continue

        if (not view.substr(t).isalnum() and not view.substr(t).isspace() and view.substr(t - 1).isalnum() and t > 0):
            pass
        else:
            t = view.find_by_class(t, forward=False, classes=WORD_END_REVERSE_STOPS)

        if t == 0:
            break

    return max(t - 1, 0)


# TODO: Move this to units.py.
def big_word_end_reverse(view, pt: int, count: int = 1) -> int:
    return word_end_reverse(view, pt, count, big=True)


def next_end_tag(view, pattern: str = RX_ANY_TAG, start: int = 0, end: int = -1) -> tuple:
    # Args:
    #   view (sublime.View)
    #   pattern (str)
    #   start (int)
    #   end (int)
    #
    # Returns:
    #   tuple[Region, str, bool]
    #   typle[None, None, None]
    region = view.find(pattern, start, IGNORECASE)
    if region.a == -1:
        return None, None, None

    match = re.search(pattern, view.substr(region))
    if match:
        return (region, match.group(1), match.group(0).startswith('</'))

    return None, None, None


def previous_begin_tag(view, pattern: str, start: int = 0, end: int = 0) -> tuple:
    assert pattern, 'bad call'
    region = reverse_search_by_pt(view, pattern, start, end, IGNORECASE)
    if not region:
        return None, None, None

    match = re.search(pattern, view.substr(region))
    if match:
        return (region, match.group(1), match.group(0)[1] != '/')

    return None, None, None


def get_region_end(r: Region) -> dict:
    return {'start': r.end()}


def get_region_begin(r: Region) -> dict:
    return {'start': 0, 'end': r.begin()}


def get_closest_tag(view, pt: int):
    # Args:
    #   view (sublime.View)
    #
    # Returns:
    #   Region|None
    substr = view.substr
    while substr(pt) != '<' and pt > 0:
        pt -= 1

    if substr(pt) != '<':
        return None

    next_tag = view.find(RX_ANY_TAG, pt)
    if next_tag.a != pt:
        return None

    return next_tag


def find_containing_tag(view, start: int) -> tuple:
    # Args:
    #   view (sublime.View)
    #
    # Returns:
    #   tuple[Region, Region, str]
    #   tuple[None, None, None]
    closest_tag = get_closest_tag(view, start)

    if not closest_tag:
        return None, None, None

    if closest_tag.contains(start) and view.substr(closest_tag)[1] == '/':
        start = closest_tag.a

    end_region, tag_name = next_unbalanced_tag(
        view,
        search=next_end_tag,
        search_args={'pattern': RX_ANY_TAG, 'start': start},
        restart_at=get_region_end
    )

    if not end_region:
        return None, None, None

    begin_region, _ = next_unbalanced_tag(
        view,
        search=previous_begin_tag,
        search_args={
            'pattern': RX_ANY_TAG_NAMED_TPL.format(tag_name),
            'start': 0,
            'end': end_region.a
        },
        restart_at=get_region_begin
    )

    if not begin_region:
        return None, None, None

    return begin_region, end_region, tag_name


def next_unbalanced_tag(view, search=None, search_args={}, restart_at=None, tags: list = []) -> tuple:
    # Args:
    #   view (sublime.View)
    #   search (callable)
    #   search_args (dict)
    #   restart_at (callable)
    #   tags (list[str])
    #
    # Returns:
    #   tuple[Region, str]
    #   tuple[None, None]
    assert search and restart_at, 'wrong call'
    region, tag, is_end_tag = search(view, **search_args)

    if not region:
        return None, None

    if not is_end_tag:
        tags.append(tag)
        search_args.update(restart_at(region))

        return next_unbalanced_tag(view, search, search_args, restart_at, tags)

    if not tags or (tag not in tags):
        return region, tag

    while tag != tags.pop():
        continue

    search_args.update(restart_at(region))

    return next_unbalanced_tag(view, search, search_args, restart_at, tags)


def find_next_item_match_pt(view, s: Region):
    pt = get_insertion_point_at_b(s)

    # Note that some item targets are added later in relevant contexts, for
    # example the item targets <> are added only when in a HTML/XML context.
    # TODO Default targets should be configurable, see :h 'matchpairs'.
    targets = '(){}[]'

    # If in a HTML/XML context, check if the cursor position is within a valid
    # tag e.g. <name>, and find the matching tag e.g. if inside an opening tag
    # then find the closing tag, if in a closing tag find the opening one.
    if view.match_selector(0, 'text.(html|xml)'):
        # Add valid HTML/XML item targets.
        targets += '<>'

        # Find matching HTML/XML items, but only if cursor is within a tag.
        if view.substr(pt) not in targets:
            closest_tag = get_closest_tag(view, pt)
            if closest_tag:
                if closest_tag.contains(pt):
                    begin_tag, end_tag, _ = find_containing_tag(view, pt)
                    if begin_tag:
                        return begin_tag.a if end_tag.contains(pt) else end_tag.a

    # Find the next item after or under the cursor.
    bracket = view_find(view, '|'.join(map(re_escape, targets)), pt)
    if not bracket:
        return

    # Only accept items found within the current cursor line.
    if bracket.b > view.line(pt).b:
        return

    target = view.substr(bracket)
    target_index = targets.index(target)
    targets_open = targets[::2]
    forward = True if target in targets_open else False

    if target in targets_open:
        target_pair = (targets[target_index], targets[target_index + 1])
    else:
        target_pair = (targets[target_index - 1], targets[target_index])

    accepted_selector = 'punctuation|text.plain'

    if forward:
        counter = 0
        start = bracket.b
        while True:
            bracket = view_find(view, '|'.join(map(re_escape, target_pair)), start)
            if not bracket:
                return

            if view.match_selector(bracket.a, accepted_selector):
                if view.substr(bracket) == target:
                    counter += 1
                else:
                    if counter == 0:
                        return bracket.a

                    counter -= 1

            start = bracket.b
    else:
        # Note the use of view_rfind_all(), because Sublime doesn't have any
        # APIs to do reverse searches and finding *all* matches before a point
        # is easier and more effiecient, at least in a userland implemention.
        counter = 0
        start = bracket.a
        for bracket in view_rfind_all(view, '|'.join(map(re_escape, target_pair)), start):
            if view.match_selector(bracket.a, accepted_selector):
                if view.substr(bracket) == target:
                    counter += 1
                else:
                    if counter == 0:
                        return bracket.a

                    counter -= 1

            start = bracket.a
