from sublime_plugin import reload_plugin


# This needs to be done to initialise sublime plugin
# commands like TextCommand and WindowCommand because
# sublime only loads .py files from the root package.
reload_plugin('NeoVintageous.tests.commands')
