from collections import defaultdict
import json
import os
import traceback

from sublime import packages_path

_session = {}
_views = defaultdict(dict)  # type: dict


def session_on_close(view) -> None:
    try:
        del _views[view.id()]
    except KeyError:
        pass


def _session_file() -> str:
    return os.path.join(os.path.dirname(packages_path()), 'Local', 'nvinfo')


def _json_object_hook_dict_str_key_to_int(x):
    if isinstance(x, dict):
        return {int(k) if k.isdigit() else k: v for k, v in x.items()}

    return x


def load_session() -> None:
    try:
        with open(_session_file(), 'r', encoding='utf=8', errors='replace') as f:
            content = f.read()
            if content.strip():
                session = json.loads(content, object_hook=_json_object_hook_dict_str_key_to_int)
                if session:
                    accept_keys = ('history', 'ex_substitute_last_pattern', 'ex_substitute_last_replacement')
                    for k, v in session.items():
                        if k not in accept_keys:
                            continue

                        # TODO The history module needs to be refactored to
                        # store it's session data in a loadable session format
                        # i.e. use session module functions to store data.
                        if k == 'history':
                            from NeoVintageous.nv.history import _storage
                            _storage.clear()
                            for _k, _v in v.items():
                                _storage[int(_k)] = _v
                        else:
                            _session[k] = v

    except FileNotFoundError:  # pragma: no cover
        pass
    except Exception:  # pragma: no cover
        traceback.print_exc()


def save_session() -> None:
    with open(_session_file(), 'w', encoding='utf-8') as f:
        session_dump = json.dumps(_session)
        f.write(session_dump)


def get_session_value(name: str, default=None):
    try:
        return _session[name]
    except KeyError:
        return default


def set_session_value(name: str, value, persist: bool = False) -> None:
    _session[name] = value

    if persist:
        save_session()


def get_session_view_value(view, name: str, default=None):
    try:
        return _views[view.id()][name]
    except KeyError:
        return default


def set_session_view_value(view, name: str, value) -> None:
    _views[view.id()][name] = value
