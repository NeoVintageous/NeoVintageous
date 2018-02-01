# Code shared between unix-like platforms (Linux and OS X).

import os
import subprocess


def run_and_wait(view, cmd, terminal_setting_name):
    term = view.settings().get(terminal_setting_name)
    term = term or os.path.expandvars("$COLORTERM") or os.path.expandvars("$TERM")
    subprocess.Popen([
        term, '-e',
        "bash -c \"%s; read -p 'Press RETURN to exit.'\"" % cmd]).wait()


def run_and_read(view, cmd):
    out, err = subprocess.Popen([cmd],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True).communicate()
    try:
        return (out or err).decode('utf-8')
    except AttributeError:
        return ''


def filter_region(view, text, command, shell_setting_name):
    shell = view.settings().get(shell_setting_name)
    shell = shell or os.path.expandvars("$SHELL")
    # Redirect STDERR to STDOUT to capture both. This seems to be the behavior
    # of vim as well.
    p = subprocess.Popen([shell, '-c', command],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    # Pass in text as input; this saves us from having to deal with quoting
    # stuff.
    out, _ = p.communicate(text.encode('utf-8'))

    return out.decode('utf-8', errors='backslashreplace')
