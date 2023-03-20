from collections import defaultdict
import json
import os
import traceback

from sublime import version
from sublime import packages_path

_session = {}

_views = defaultdict(dict)  # type: dict


_VERSION = int(version())

# Saving the session on exit is only available in newer builds. Otherwise
# sessions are saved in realtime which is a performance concern.
if _VERSION >= 4081:

    # Saving sessions needs to use the Sublime packages path API but the API is
    # not available when the application is shutting down and access to the
    # packages path API is only available at import time from build 4081.
    _PACKAGES_PATH = packages_path()

    def get_packages_path() -> str:
        return _PACKAGES_PATH

    def session_on_exit() -> None:
        save_session()

    # In newer builds the session is saved when exiting Sublime.
    def maybe_do_runtime_save_session() -> None:
        pass
else:
    def get_packages_path() -> str:
        return packages_path()

    def session_on_exit() -> None:
        pass

    def maybe_do_runtime_save_session() -> None:
        save_session()


def _get_session_file() -> str:
    return os.path.join(
        os.path.dirname(get_packages_path()),
        'Local',
        'neovintageous.session'
    )


def session_on_close(view) -> None:
    try:
        del _views[view.id()]
    except KeyError:
        pass


def _recursively_convert_dict_digit_keys_to_int(value) -> dict:
    if not isinstance(value, dict):
        return value

    return dict((
        int(k) if k.isdigit() else k, _recursively_convert_dict_digit_keys_to_int(v)
    ) for k, v in value.items())


def load_session() -> None:
    try:
        with open(_get_session_file(), 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if content.strip():
                session = json.loads(content)
                if session:
                    accept_keys = (
                        'history',
                        'ex_substitute_last_pattern',
                        'ex_substitute_last_replacement',
                        'last_used_register_name',
                        'macros',
                    )

                    for k, v in session.items():
                        if k not in accept_keys:
                            continue

                        # TODO Refactor history module to be session friendly.
                        if k == 'history':
                            # Import inline to avoid circular reference.
                            from NeoVintageous.nv.history import _storage
                            _storage.clear()
                            for _k, _v in v.items():
                                # The session is stored in JSON format and json
                                # dump serialized dict int keys as strings. So
                                # the keys need to be deserialized to ints.
                                _storage[int(_k)] = _recursively_convert_dict_digit_keys_to_int(_v)

                            # history is a special case.
                            continue

                        _session[k] = v

    except FileNotFoundError:
        pass
    except Exception:  # pragma: no cover
        traceback.print_exc()


def save_session() -> None:
    with open(_get_session_file(), 'w', encoding='utf-8') as f:
        f.write(json.dumps(_session))


def get_session_value(name: str, default=None):
    try:
        return _session[name]
    except KeyError:
        # Set session default value now before returning the value because it
        # could be a mutable type e.g. dict, list, set.
        _session[name] = default

        return _session[name]


def set_session_value(name: str, value, persist: bool = False) -> None:
    _session[name] = value

    if persist:
        maybe_do_runtime_save_session()


def get_session_view_value(view, name: str, default=None):
    try:
        return _views[view.id()][name]
    except KeyError:
        return default


def set_session_view_value(view, name: str, value) -> None:
    _views[view.id()][name] = value
