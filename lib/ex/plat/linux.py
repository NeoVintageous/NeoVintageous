from NeoVintageous.lib.ex.plat import unixlike


def run_and_wait(view, cmd):
    unixlike.run_and_wait(view, cmd, 'VintageousEx_linux_terminal')


def run_and_read(view, cmd):
    return unixlike.run_and_read(view, cmd)


def filter_region(view, text, command):
    return unixlike.filter_region(
        view, text, command, 'VintageousEx_linux_shell')
