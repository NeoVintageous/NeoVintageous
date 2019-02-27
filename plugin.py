# Copyright (C) 2018 The NeoVintageous Team (NeoVintageous).
#
# This file is part of NeoVintageous.
#
# NeoVintageous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeoVintageous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeoVintageous.  If not, see <https://www.gnu.org/licenses/>.

import os

# If debugging is enabled, initialise the debug logger.
#
# The debug logger needs to be configured before plugin modules are loaded,
# otherwise the plugins would end up logging to a non-existing logger (a null
# logger; Python configures a "handler of last resort" since 3.2, which is a
# StreamHandler writing to sys.stderr with a level of WARNING, and is used to
# handle logging events in the absence of any logging configuration. The end
# result is to just print the message to sys.stderr, and in Sublime Text that
# means it will print the message to console.
#
# To enable debugg logging:
#
# Set an environment variable named SUBLIME_NEOVINTAGEOUS_DEBUG.
if bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG')):
    import logging

    logger = logging.getLogger('NeoVintageous')

    # Avoid duplicate loggers when plugin is reloaded.
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            'NeoVintageous: %(levelname)-7s [%(filename)s:%(lineno)d] %(message)s'
        ))
        logger.addHandler(stream_handler)
        logger.debug('debug logger initialised')

import sublime  # noqa: E402

# The plugin loading is designed to handle errors gracefully.
#
# When upgrading the plugin, changes to the plugin structure can cause import
# errors. In these cases we want to notify the user about needing to restart
# Sublime Text to finish the upgrade.
#
# In the case of any errors we don't want to leave the normal functioning of the
# editor unusable. We can't access the sublime api until the plugin_loaded()
# hook is called, so we need to catch any exceptions and run cleanup operations
# when the plugin_loaded() hook is called.

try:
    _startup_exception = None

    # Commands.
    from NeoVintageous.nv.commands import *  # noqa: F401,F403

    # Plugins.
    from NeoVintageous.nv.plugin_abolish import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_commentary import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_surround import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_unimpaired import *  # noqa: F401,F403

    # Events.
    from NeoVintageous.nv.events import *  # noqa: F401,F403

except Exception as e:
    import traceback
    traceback.print_exc()
    _startup_exception = e


def _update_ignored_packages():

    # Updates the list of ignored packages with packages that are redundant,
    # obsolete, or cause problems due to conflicts e.g. Vintage, Vintageous,
    # etc.

    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])
    conflict_packages = [x for x in ['Six', 'Vintage', 'Vintageous'] if x not in ignored_packages]
    if conflict_packages:
        print('NeoVintageous: update ignored packages with conflicts {}'.format(conflict_packages))
        ignored_packages = sorted(ignored_packages + conflict_packages)
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')


def _cleanup_views():

    # Resets cursor and mode. In the case of errors loading the plugin this can
    # help prevent the normal functioning of editor becoming unusable e.g. the
    # cursor getting stuck in a block shape or the mode getting stuck in normal
    # or visual mode.

    for window in sublime.windows():
        for view in window.views():
            settings = view.settings()
            settings.set('command_mode', False)
            settings.set('inverse_caret_state', False)
            settings.erase('vintage')


def plugin_loaded():

    # Enable sublime debug information if in DEBUG mode.
    if bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG')):
        sublime.log_input(True)
        sublime.log_commands(True)

    loading_exeption = None

    pc_event = None

    try:
        from package_control import events
        if events.install('NeoVintageous'):
            pc_event = 'install'
        if events.post_upgrade('NeoVintageous'):
            pc_event = 'post_upgrade'
    except ImportError:
        pass  # Package Control isn't available (PC is not required)
    except Exception as e:
        import traceback
        traceback.print_exc()
        loading_exeption = e

    try:
        _update_ignored_packages()
    except Exception as e:
        import traceback
        traceback.print_exc()
        loading_exeption = e

    try:
        from NeoVintageous.nv import rc
        rc.load()
    except Exception as e:
        import traceback
        traceback.print_exc()
        loading_exeption = e

    if _startup_exception or loading_exeption:

        try:
            _cleanup_views()
        except Exception:
            import traceback
            traceback.print_exc()

        if isinstance(_startup_exception, ImportError) or isinstance(loading_exeption, ImportError):
            if pc_event == 'post_upgrade':
                message = "Failed to load some modules trying to upgrade NeoVintageous. "\
                          "Please restart Sublime Text to finish the upgrade."
            else:
                message = "Failed to load some NeoVintageous modules. "\
                          "Please restart Sublime Text."
        else:
            if pc_event == 'post_upgrade':
                message = "An error occurred trying to upgrade NeoVintageous. "\
                          "Please restart Sublime Text to finish the upgrade."
            else:
                message = "An error occurred trying to load NeoVintageous. "\
                          "Please restart Sublime Text."

        print('NeoVintageous: ERROR', message)
        sublime.message_dialog(message)


def plugin_unloaded():

    try:
        _cleanup_views()
    except Exception:
        import traceback
        traceback.print_exc()
