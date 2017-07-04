import re

from sublime import Region

from NeoVintageous.lib.nvim import message


_MODELINES_MAX_LINE_LEN = 80
_PREFIX_TPL = '%s\\s*(st|sublime): '
_DEFAULT_LINE_COMMENT = '#'
_MULTIOPT_SEP = '; '


def _gen_modelines(view, modelines):
    # Args:
    #   view (sublime.View):
    #   modelines (int): Number of modelines to check.
    #
    # Return:
    #   list
    max_pts = modelines * _MODELINES_MAX_LINE_LEN

    to_pt = view.text_point(modelines, 0)
    to_pt = min(to_pt, max_pts)

    candidates = view.lines(Region(0, to_pt))

    view_size = view.size()
    last_line_number = view.rowcol(view_size)[0]
    if last_line_number >= modelines:
        from_pt = view.text_point(max(last_line_number - modelines, modelines), 0)
        from_pt = max(from_pt, (view_size - max_pts))
        candidates += view.lines(Region(from_pt, view.size()))

    prefix = _build_modeline_prefix(view)
    modelines = (view.substr(c) for c in candidates if re.match(prefix, view.substr(c)))

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
    modelines = _gen_modelines(view, view.settings().get('vintageous_modelines'))
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

    return (_PREFIX_TPL % lineComment)


def _to_json_type(v):
    # Convert string value to proper JSON type.
    #
    # Args:
    #   v (sublime.View):
    if v.lower() in ('true', 'false'):
        v = v[0].upper() + v[1:].lower()

    try:
        return eval(v, {}, {})
    except Exception:
        raise ValueError('could not convert to JSON type')


def do_modeline(view):
    # A feature similar to vim modeline.
    #
    # A number of lines at the beginning and end of the file are checked for
    # modelines.
    #
    # See :help auto-setting for more information.
    #
    # Args:
    #   view (sublime.View)
    #
    # Example:
    #     # sublime: gutter false
    #     # sublime: translate_tab_to_spaces true
    #     # sublime: rulers [80, 120]
    #     # sublime: tab_size 4
    for setter, name, value in _gen_modeline_options(view):
        if name == 'x_syntax':
            view.set_syntax_file(value)
        else:
            try:
                setter(name, _to_json_type(value))
            except ValueError as e:
                message('Error detected while processing modelines: option = {}'.format(name))
