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

from collections import namedtuple

from NeoVintageous.nv.vi.utils import translate_char
from NeoVintageous.nv.vim import INPUT_IMMEDIATE
from NeoVintageous.nv.vim import INPUT_VIA_PANEL


parser_def = namedtuple('parsed_def', 'command interactive_command input_param on_done type')


def get(state, name):
    parser_func = globals().get(name, None)
    if parser_func is None:
        raise ValueError('parser name unknown')

    return parser_func(state)


# TODO [refactor] Rename parameter name to something more descriptive.
def one_char(in_):
    # Any input (character) satisfies this parser.
    #
    # Args:
    #   in_ (str):
    #
    # Returns
    #   bool: True if in_ is one character in length, False otherwise.
    return len(translate_char(in_)) == 1


# TODO [refactor] Maybe refactoring the required {state} parameter of all the
# following functions, because none of them require the {state}. Some of the
# functions require a boolean "interactive" parameter.


def vi_f(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_big_f(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_big_t(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_t(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


# TODO [refactor] Rename to "vi_a_text_object".
def vi_inclusive_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_exclusive_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_m(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_q(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_at(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_a_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_i_text_object(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_quote(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_r(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done='_vi_r_on_parser_done',
                      type=INPUT_IMMEDIATE)


def vi_backtick(state):
    return parser_def(command=one_char,
                      interactive_command=None,
                      input_param=None,
                      on_done=None,
                      type=INPUT_IMMEDIATE)


def vi_slash(state):
    # Parse should always be used non-interactively.
    #
    # '/' usually collects its input from an input panel.
    #
    # Any input is valid; we're never satisfied.
    #
    # Args:
    #   state (NeoVintageous.nv.State):
    #
    # Returns:
    #   A named 5-tuple.
    if state.non_interactive:
        return parser_def(command=lambda x: False,
                          interactive_command='_vi_slash',
                          type=INPUT_IMMEDIATE,
                          on_done='_vi_slash_on_parser_done',
                          input_param='key')
    else:
        return parser_def(command='_vi_slash',
                          interactive_command='_vi_slash',
                          type=INPUT_VIA_PANEL,
                          on_done=None,
                          input_param='default')


def vi_question_mark(state):
    # Parser should always be used non-interactively.
    #
    # '?' usually collects its input from an input panel.
    #
    # Any input is valid; we're never satisfied.
    #
    # Args:
    #   state (NeoVintageous.nv.State):
    #
    # Returns:
    #   A named 5-tuple.
    if state.non_interactive:
        return parser_def(command=lambda x: False,
                          interactive_command='_vi_question_mark',
                          type=INPUT_IMMEDIATE,
                          on_done='_vi_question_mark_on_parser_done',
                          input_param='key')
    else:
        return parser_def(command='_vi_question_mark',
                          interactive_command='_vi_question_mark',
                          type=INPUT_VIA_PANEL,
                          on_done=None,
                          input_param='default')
