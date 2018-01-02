# CONTRIBUTING

## Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests.

Install it, open the Command Palette, type "UnitTesting", press Enter, and input "NeoVintageous" as the package to test.

## Debugging

The Sublime Text startup log is found in the console: `Menu > View > Show Console`.

Command and input logging can be enabled from the console (run the commands in input box at the bottom of the console): `sublime.log_commands(True)` for command logging, and `sublime.log_input(True)` input logging.

Neovintageous debug messages are disabled by default. You can enable them by setting an environment variable named `SUBLIME_NEOVINTAGEOUS_DEBUG` to a non-blank value. See [set a Sublime Text environment variable](https://github.com/gerardroche/sublime-phpunit#debugging) for a step by step guide on how to set environment variables for Sublime Text. The debug log is located at `Packages/User/NeoVintageous.log`. Debug messages are also printed to the console: `Menu > View > Show Console`.

### Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

For Linux and OSX, [this shell script](https://github.com/gerardroche/dotfiles/blob/7f7812393e26db7c0f8146f5b6db730197dfd103/src/bin/sublime-clean), can be used to clean caches, indexes, workspaces, sessions, etc. Note that cleaning and reverting are two different things: *reverting* will remove installed packages and configurations, *cleaning* will only remove files generated at runtime by Sublime Text e.g. caches, indexes, workspaces, sessions.
