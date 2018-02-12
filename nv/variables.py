
_special_strings = {
    '<leader>': 'mapleader',
    '<localleader>': 'maplocalleader',
}


_defaults = {
    'mapleader': '\\',
    'maplocalleader': '\\'
}


_variables = {}


def expand_keys(seq):
    # type: (str) -> str
    seq_lower = seq.lower()
    for key, key_value, in _special_strings.items():
        while key in seq_lower:
            index = seq_lower.index(key)
            value = _variables.get(key_value, _defaults.get(key_value))
            if value:
                seq = seq[:index] + value + seq[index + len(key):]
                seq_lower = seq.lower()
            else:

                # XXX This is a safe guard against infinite loop. Ideally
                # special keys that have no default or variable values should
                # just be replaced as-is, that will require reworking this
                # function.

                return seq

    return seq


def is_key_name(name):
    # type: (str) -> bool
    return name.lower() in _special_strings


def get(name):
    # type: (str) -> str
    name = name.lower()
    name = _special_strings.get(name, name)

    return _variables.get(name, _defaults.get(name))


def set(name, value):
    # type: (...) -> None
    _variables[name] = value
