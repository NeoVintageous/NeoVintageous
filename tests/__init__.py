import sublime_plugin


# This needs to be done to initialise sublime plugin
# commands like TextCommand and WindowCommand because
# sublime only loads .py files from the root package.
sublime_plugin.reload_plugin('NeoVintageous.tests.commands')
