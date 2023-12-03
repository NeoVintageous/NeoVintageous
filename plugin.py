# Copyright (C) 2018-2023 The NeoVintageous Team (NeoVintageous).
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

import logging
import os
import traceback

# The logger needs to be configured before any modules are loaded.
logger = logging.getLogger(__package__)
logger.propagate = False

# To enable debug logging set the following environment variable to a non-blank
# value or to a logging level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET.
_DEBUG = os.getenv('SUBLIME_NEOVINTAGEOUS_DEBUG')
if _DEBUG:
    logger.setLevel(getattr(logging, _DEBUG.upper(), logging.DEBUG))
else:
    logger.setLevel(logging.WARNING)

# Avoid duplicate loggers e.g., if the plugin is reloaded.
if not logger.hasHandlers():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(
        'NeoVintageous.%(levelname)-7s [%(filename)15s:%(lineno)-4d] %(message)s'
    ))
    logger.addHandler(stream_handler)

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
    from NeoVintageous.nv.plugin_input_method import *  # noqa: F401,F403
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

    if int(sublime.version()) >= 3143:
        # In Package Control 4, orphaned packages, e.g., packages listed as
        # ignored, but not actually installed, are pruned. So only packages
        # that actually installed should be considered as conflicting.
        installed_packages = sublime.load_settings('Package Control.sublime-settings').get('installed_packages', [])
        conflict_candidates = [p for p in ['Six', 'Vintageous'] if p in installed_packages]
        # The Vintage is bundled with ST so it is always installed.
        conflict_candidates.append('Vintage')
    else:
        conflict_candidates = ['Six', 'Vintage', 'Vintageous']

    settings = sublime.load_settings('Preferences.sublime-settings')
    ignored_packages = settings.get('ignored_packages', [])
    if not isinstance(ignored_packages, list):
        ignored_packages = []
    conflict_packages = [x for x in conflict_candidates if x not in ignored_packages]
    if conflict_packages:  # pragma: no cover
        print('NeoVintageous: update ignored packages with conflicts {}'.format(conflict_packages))
        ignored_packages = sorted(ignored_packages + conflict_packages)
        settings.set('ignored_packages', ignored_packages)
        sublime.save_settings('Preferences.sublime-settings')


def _init_backwards_compat_patches():

    # Some setting defaults are changed from time to time. To reduce the impact
    # on users, their current preferences are updated so that when the default
    # is changed later, their preferences will be override the new default.

    try:
        preferences = sublime.load_settings('Preferences.sublime-settings')

        # The build number is in the format {major}{minor}{patch}, where the
        # major number is one digit, minor two digits, and patch two digits.
        #
        #   Version | Build (as integer)
        #   ------- | -----
        #   1.11.0  | 11100
        #   1.11.3  | 11103
        #   1.17.1  | 11701
        #   1.27.0  | 12700

        build_version = preferences.get('neovintageous_build_version', 0)
        if not isinstance(build_version, int):
            build_version = 0

        if build_version < 12700:  # pragma: no cover

            preferences.set('neovintageous_build_version', 12700)
            old_file = os.path.join(os.path.dirname(sublime.packages_path()), 'Local', 'nvinfo')
            new_file = os.path.join(os.path.dirname(sublime.packages_path()), 'Local', 'neovintageous.session')
            if os.path.exists(old_file) and not os.path.exists(new_file):
                os.rename(old_file, new_file)

            sublime.save_settings('Preferences.sublime-settings')

        if build_version < 13200:  # pragma: no cover
            if build_version != 0:
                try:
                    # The super are now enabled by default. To avoid disruption
                    # to users, when upgrading, the super keys are set to false
                    # for users who have not already enabled them.
                    settings = sublime.decode_value(sublime.load_resource('Packages/User/Preferences.sublime-settings'))
                    use_super_keys = settings.get('vintageous_use_super_keys')  # type: ignore[union-attr]
                    if use_super_keys is None:
                        preferences.set('vintageous_use_super_keys', False)
                except Exception:
                    traceback.print_exc()

            preferences.set('neovintageous_build_version', 13200)
            sublime.save_settings('Preferences.sublime-settings')

    except Exception:  # pragma: no cover
        traceback.print_exc()


def plugin_loaded():

    _init_backwards_compat_patches()

    loading_exeption = None
    package_control_event = None

    try:
        from package_control import events
        if events.install('NeoVintageous'):  # pragma: no cover
            package_control_event = 'install'
        if events.post_upgrade('NeoVintageous'):  # pragma: no cover
            package_control_event = 'post_upgrade'
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
            if package_control_event == 'post_upgrade':
                message = "Failed to load some modules trying to upgrade NeoVintageous. "\
                          "Please restart Sublime Text to finish the upgrade."
            else:
                message = "Failed to load some NeoVintageous modules. "\
                          "Please restart Sublime Text."
        else:
            if package_control_event == 'post_upgrade':
                message = "An error occurred trying to upgrade NeoVintageous. "\
                          "Please restart Sublime Text to finish the upgrade."
            else:
                message = "An error occurred trying to load NeoVintageous. "\
                          "Please restart Sublime Text."

        print('NeoVintageous: ERROR', message)
        sublime.message_dialog(message)


def plugin_unloaded():
    clean_views()
