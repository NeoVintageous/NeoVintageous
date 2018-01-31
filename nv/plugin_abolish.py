import re

from sublime_plugin import TextCommand

from NeoVintageous.nv.plugin import INPUT_INMEDIATE
from NeoVintageous.nv.plugin import inputs
from NeoVintageous.nv.plugin import NORMAL
from NeoVintageous.nv.plugin import register
from NeoVintageous.nv.plugin import ViOperatorDef


__all__ = [
    '_nv_abolish_command'
]


# A port of https://github.com/tpope/vim-abolish.


def _coerce_to_mixedcase(string):
    return _coerce_to_spacecase(string).title().replace(' ', '')


def _coerce_to_camelcase(string):
    string = _coerce_to_spacecase(string).title().replace(' ', '')
    if len(string) > 1:
        return string[0].lower() + string[1:]
    return string.lower()


def _coerce_to_snakecase(string):
    # https://stackoverflow.com/a/1176023
    # https://github.com/jpvanhal/inflection
    string = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', string)
    string = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', string)
    string = string.replace("-", "_")
    return string.lower()


def _coerce_to_uppercase(string):
    return _coerce_to_snakecase(string).upper()


def _coerce_to_dashcase(string):
    return _coerce_to_snakecase(string).replace('_', '-')


def _coerce_to_spacecase(string):
    return _coerce_to_snakecase(string).replace('_', ' ')


def _coerce_to_dotcase(string):
    return _coerce_to_snakecase(string).replace('_', '.')


def _coerce_to_titlecase(string):
    return _coerce_to_spacecase(string).title()


_COERCIONS = {
    'mixedcase': _coerce_to_mixedcase,
    'camelcase': _coerce_to_camelcase,
    'snakecase': _coerce_to_snakecase,
    'uppercase': _coerce_to_uppercase,
    'dashcase': _coerce_to_dashcase,
    'spacecase': _coerce_to_spacecase,
    'dotcase': _coerce_to_dotcase,
    'titlecase': _coerce_to_titlecase
}


_ALIASES = {
    'm': 'mixedcase',
    'c': 'camelcase',
    '_': 'snakecase',
    's': 'snakecase',
    'u': 'uppercase',
    'U': 'uppercase',
    '-': 'dashcase',
    'k': 'dashcase',
    '<space>': 'spacecase',
    '.': 'dotcase',
    't': 'titlecase'
}


@register(seq='cr', modes=(NORMAL,))
class _AbolishCoercions(ViOperatorDef):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scroll_into_view = True
        self.updates_xpos = True
        self.input_parser = inputs.parser_def(
            command=inputs.one_char,
            interactive_command=None,
            input_param=None,
            on_done=None,
            type=INPUT_INMEDIATE
        )

    @property
    def accept_input(self):
        return self.inp == ''

    def accept(self, key):
        self._inp = key

        return True

    def translate(self, state):
        return {
            'action': '_nv_abolish',
            'action_args': {
                'to': self.inp
            }
        }


class _nv_abolish_command(TextCommand):
    def run(self, edit, to=None, mode=None):

        if to in _ALIASES:
            to = _ALIASES[to]

        if to in _COERCIONS:
            coerce_func = _COERCIONS[to]
        else:
            raise ValueError('unknown coercion')

        new_sels = []
        for sel in self.view.sel():
            if sel.empty():
                sel = self.view.word(sel)

            new_sels.append(sel.begin())

            self.view.replace(edit, sel, coerce_func(self.view.substr(sel)))

        if new_sels:
            self.view.sel().clear()
            self.view.sel().add_all(new_sels)
