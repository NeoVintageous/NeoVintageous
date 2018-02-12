from NeoVintageous.nv import shell_unixlike


def run_and_wait(view, cmd):
    # type: (...) -> None
    shell_unixlike.run_and_wait(view, cmd, 'VintageousEx_linux_terminal')


def run_and_read(view, cmd):
    # type: (...) -> str
    return shell_unixlike.run_and_read(view, cmd)


def filter_region(view, text, command):
    # type: (...) -> str
    return shell_unixlike.filter_region(view, text, command, 'VintageousEx_linux_shell')
