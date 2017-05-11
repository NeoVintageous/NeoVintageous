import re

import sublime


_MODELINE_PREFIX_TPL = "%s\\s*(st|sublime): "
_DEFAULT_LINE_COMMENT = '#'
_MULTIOPT_SEP = '; '
_MAX_LINES_TO_CHECK = 50
_LINE_LENGTH = 80
_MODELINES_REG_SIZE = _MAX_LINES_TO_CHECK * _LINE_LENGTH


def _is_modeline(prefix, line):
    return bool(re.match(prefix, line))


def _gen_modelines(view):
    topRegEnd = min(_MODELINES_REG_SIZE, view.size())
    candidates = view.lines(sublime.Region(0, view.full_line(topRegEnd).end()))

    # Consider modelines at the end of the buffer too. There might be overlap
    # with the top region, but it doesn't matter because it means the buffer is
    # tiny.
    pt = view.size() - _MODELINES_REG_SIZE
    bottomRegStart = pt if pt > -1 else 0
    candidates += view.lines(sublime.Region(bottomRegStart, view.size()))

    prefix = _build_modeline_prefix(view)
    modelines = (view.substr(c) for c in candidates if _is_modeline(prefix, view.substr(c)))

    for modeline in modelines:
        yield modeline


def _gen_raw_options(modelines):
    for m in modelines:
        opt = m.partition(':')[2].strip()
        if _MULTIOPT_SEP in opt:
            for subopt in (s for s in opt.split(_MULTIOPT_SEP)):
                yield subopt
        else:
            yield opt


def _gen_modeline_options(view):
    modelines = _gen_modelines(view)
    for opt in _gen_raw_options(modelines):
        name, sep, value = opt.partition(' ')
        yield view.settings().set, name.rstrip(':'), value.rstrip(';')


def _get_line_comment_char(view):
    commentChar = ""
    commentChar2 = ""
    try:
        for pair in view.meta_info("shellVariables", 0):
            if pair["name"] == "TM_COMMENT_START":
                commentChar = pair["value"]
            if pair["name"] == "TM_COMMENT_START_2":
                commentChar2 = pair["value"]
            if commentChar and commentChar2:
                break
    except TypeError:
        pass

    if not commentChar2:
        return re.escape(commentChar.strip())
    else:
        return "(" + re.escape(commentChar.strip()) + "|" + re.escape(commentChar2.strip()) + ")"


def _build_modeline_prefix(view):
    lineComment = _get_line_comment_char(view).lstrip() or _DEFAULT_LINE_COMMENT
    return (_MODELINE_PREFIX_TPL % lineComment)


def _to_json_type(v):
    """Convert string value to proper JSON type."""
    if v.lower() in ('true', 'false'):
        v = v[0].upper() + v[1:].lower()

    try:
        return eval(v, {}, {})
    except:
        raise ValueError("Could not convert to JSON type.")


def modelines(view):
    for setter, name, value in _gen_modeline_options(view):
        if name == 'x_syntax':
            view.set_syntax_file(value)
        else:
            try:
                setter(name, _to_json_type(value))
            except ValueError as e:
                sublime.status_message("NeoVintageous: bad modeline detected")
                print("NeoVintageous: bad option detected {name = %s, value = %s}" % (name, value))
                print("NeoVintageous: (tip) keys cannot be empty strings")
