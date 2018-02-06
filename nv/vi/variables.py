
_SPECIAL_STRINGS = {
    '<leader>': 'mapleader',
    '<localleader>': 'maplocalleader',
}


_DEFAULTS = {
    'mapleader': '\\',
    'maplocalleader': '\\'
}


_VARIABLES = {
}


def expand_keys(seq):
    seq_lower = seq.lower()
    for key, key_value, in _SPECIAL_STRINGS.items():
        while key in seq_lower:
            index = seq_lower.index(key)
            value = _VARIABLES.get(key_value, _DEFAULTS.get(key_value))
            if value:
                seq = seq[:index] + value + seq[index + len(key):]
                seq_lower = seq.lower()

    return seq


def is_key_name(name):
    return name.lower() in _SPECIAL_STRINGS


def get(name):
    name = name.lower()
    name = _SPECIAL_STRINGS.get(name, name)

    return _VARIABLES.get(name, _DEFAULTS.get(name))


def set_(name, value):
    _VARIABLES[name] = value


class Variables(object):

    def __get__(self, instance, owner):
        self.view = instance.view
        self.settings = instance.settings

        return self

    def get(self, name):
        return get(name)

    def set(self, name, value):
        return set_(name, value)
