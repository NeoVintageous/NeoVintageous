from NeoVintageous.nv.ex.plat import unixlike


def run_and_wait(view, cmd):
    unixlike.run_and_wait(view, cmd, 'VintageousEx_osx_terminal')


def run_and_read(view, cmd):
    return unixlike.run_and_read(view, cmd)


def filter_region(view, text, command):
    return unixlike.filter_region(
        view, text, command, 'VintageousEx_osx_shell')
