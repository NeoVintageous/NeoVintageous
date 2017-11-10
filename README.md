![NeoVintageous Logo](res/neovintageous.png)

An advanced Vim emulation layer for Sublime Text.

[![Build Status](https://img.shields.io/travis/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://travis-ci.org/NeoVintageous/NeoVintageous) [![Build status](https://img.shields.io/appveyor/ci/gerardroche/neovintageous/master.svg?style=flat-square)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Coverage Status](https://img.shields.io/coveralls/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://coveralls.io/github/NeoVintageous/NeoVintageous?branch=master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?style=flat-square&label=stable)](https://github.com/NeoVintageous/NeoVintageous/tags) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Downloads](https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square)](https://packagecontrol.io/packages/NeoVintageous)

Neovintageous is a project that seeks to continue the development of the discontinued Vintageous as an open source project.

* Open source
* Highly configurable
* Plugins out-of-the-box
* Strong defaults
* Drop-in replacement for Vintageous
* Integrates with [GitGutter](https://github.com/jisaacks/GitGutter), [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) and [Origami](https://github.com/SublimeText/Origami)

## Installation

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/browse/authors/NeoVintageous).

### Manual installation

Close Sublime Text, then download or clone this repository to a directory named `NeoVintageous` in the Sublime Text Packages directory for your platform:

* Linux: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`
* OSX: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`
* Windows: `git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`

## Documentation

Neovintageous is an emulation of Vim: feature-parity is an ongoing effort. See the [`:help neovintageous`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) command to learn about the differences.

Vim's documentation system is accessible via the `:help` command, and is an extensive cross-referenced and hyperlinked reference. It's kept up-to-date with the software and can answer almost any question about Vim's functionality. An up-to-date version of Vim help, with hyperlinks, can be found on [appspot](https://vimhelp.appspot.com).

## Contributing

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "NeoVintageous" as the package to test.

### Debugging

The Sublime Text startup log can be found in the console: `Menu > View > Show Console`.

Command and input logging can be enabled from the console: `sublime.log_commands(True); sublime.log_input(True)` (run the commands in input box at the bottom of the console panel via `Menu > View > Show Console`). Other logging such as regex results, indexing, and build systems can be enabled too: `sublime.log_result_regex(True); sublime.log_indexing(True); sublime.log_build_systems(True)`.

Neovintageous debug messages are disabled by default. You can enable them by setting an environment variable named `SUBLIME_NEOVINTAGEOUS_DEBUG` to a non-blank value. See [set a Sublime Text environment variable](https://github.com/gerardroche/sublime-phpunit#debugging) for a step by step guide on how to set environment variables for Sublime Text. The debug log is located at `Packages/User/NeoVintageous.log`. Debug messages are also printed to the console: `Menu > View > Show Console`.

#### Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

For Linux and OSX [this script](https://github.com/gerardroche/dotfiles/blob/7f7812393e26db7c0f8146f5b6db730197dfd103/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Note that cleaning and reverting are two different things, *reverting* will remove installed packages and configurations, whereas *cleaning* will only remove files generated by Sublime Text at runtime like caches, indexes, workspaces, sessions, etc.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Acknowledgements

Neovintageous is a fork of the discontinued [Vintageous](https://github.com/guillermooo/Vintageous).

## License

Released under the [MIT License](LICENSE).
