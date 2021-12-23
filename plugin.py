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
import traceback

# To enable debug logging, set the env var to a non-blank value.
_DEBUG = bool(os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG'))

# If debugging is enabled, initialise the debug logger. The debug logger needs
# to be configured before any plugin modules are loaded, otherwise the plugins
# would send log messages to a "handler of last resort". The "handler of last
# resort" is a logger that python configures in the absence of any logging
# configuration (a StreamHandler that writes to sys.stderr with a level of
# WARNING. The end result is that it prints the message to sys.stderr, and in
# Sublime Text that means it will print the message to console).
if _DEBUG:  # pragma: no cover
    import logging

    logger = logging.getLogger('NeoVintageous')

    # Avoid duplicate loggers when the plugin is reloaded.
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            'NeoVintageous: %(levelname)-7s [%(filename)15s:%(lineno)4d] %(message)s'
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

    from NeoVintageous.nv.rc import load_rc
    from NeoVintageous.nv.session import load_session
    from NeoVintageous.nv.vim import clean_views

    # Commands.
    from NeoVintageous.nv.commands import *  # noqa: F401,F403

    # Plugins.
    from NeoVintageous.nv.plugin_abolish import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_commentary import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_multiple_cursors import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_sneak import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_sublime import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_surround import *  # noqa: F401,F403
    from NeoVintageous.nv.plugin_unimpaired import *  # noqa: F401,F403

    # Events.
    from NeoVintageous.nv.events import *  # noqa: F401,F403

except Exception as e:  # pragma: no cover
    traceback.print_exc()
    _startup_exception = e


def _update_ignored_packages():

    # Updates the list of ignored packages with packages that are redundant,
    # obsolete, or cause problems due to conflicts e.g. Vintage, Vintageous,
    # etc.

    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])
    conflict_packages = [x for x in ['Six', 'Vintage', 'Vintageous'] if x not in ignored_packages]
    if conflict_packages:  # pragma: no cover
        print('NeoVintageous: update ignored packages with conflicts {}'.format(conflict_packages))
        ignored_packages = sorted(ignored_packages + conflict_packages)
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')


def _init_backwards_compat_patches():

    # Some setting defaults are changed from time to time. To reduce the impact
    # on users, their current preferences are updated so that when the default
    # is changed later, their preferences will be override the new default.
    # See: https://github.com/NeoVintageous/NeoVintageous/issues/404.
    # TODO Remove all backwards compatability settings updates in future version

    try:

        preferences = sublime.load_settings('Preferences.sublime-settings')

        # The build number is in the format {MAJOR}{MINOR}{PATCH}, where the
        # major number if one digit, the minor two digits, and the patch two
        # digits e.g. 1.11.0 -> 11100, 1.11.3 -> 11103, 1.17.1 -> 11701.
        build_version = int(preferences.get('neovintageous_build_version', 0))

        if build_version < 11100:  # pragma: no cover
            preferences.set('neovintageous_build_version', 11100)
            # Migrate the ".vintageousrc" (runtime configuation) file. The new
            # file name is ".neovintageousrc" and is automatically renamed to
            # the new name to avoid disruption to users.
            old_file = os.path.join(sublime.packages_path(), 'User', '.vintageousrc')
            new_file = os.path.join(sublime.packages_path(), 'User', '.neovintageousrc')
            if os.path.exists(old_file):
                if os.path.exists(new_file):
                    print('NeoVintageous: could not migrate "%s" to "%s": target already exists' % (old_file, new_file))  # noqa: E501
                else:
                    os.rename(old_file, new_file)

            sublime.save_settings('Preferences.sublime-settings')
    except Exception:  # pragma: no cover
        traceback.print_exc()


def plugin_loaded():
    if _DEBUG:  # pragma: no cover
        sublime.log_input(True)
        sublime.log_commands(True)

    _init_backwards_compat_patches()

    loading_exeption = None

    pc_event = None

    try:
        from package_control import events
        if events.install('NeoVintageous'):  # pragma: no cover
            pc_event = 'install'
        if events.post_upgrade('NeoVintageous'):  # pragma: no cover
            pc_event = 'post_upgrade'
    except ImportError:  # pragma: no cover
        pass  # Package Control isn't available (PC is not required)
    except Exception as e:  # pragma: no cover
        traceback.print_exc()
        loading_exeption = e

    try:
        _update_ignored_packages()
    except Exception as e:  # pragma: no cover
        traceback.print_exc()
        loading_exeption = e

    try:
        load_session()
        load_rc()
    except Exception as e:  # pragma: no cover
        traceback.print_exc()
        loading_exeption = e

    if _startup_exception or loading_exeption:  # pragma: no cover

        clean_views()

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
    clean_views()
