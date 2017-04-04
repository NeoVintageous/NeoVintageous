# WHAT IS &lt;package name&gt;

[![Build Status](https://travis-ci.org/gerardroche/Vintageous.svg?branch=master)](https://travis-ci.org/gerardroche/Vintageous)

A comprehensive vi/Vim emulation layer for Sublime Text 3.

**This is a fork of Vintageous and is currently under active development. It will be re-branded with a name (which has yet to be chosen) and published in the Package Control in the next few weeks. Your ideas for a new name are welcome.**

[![Rick Astley - Never Gonna Give You Up](rickroll.png)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## OVERVIEW

* [Installation](#installation)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## CONFIGURATION

Key | Description | Type | Default
----|-------------|------|--------
`vintageous_autoindent` | Enable auto indentation. | `boolean` | `true`
`vintageous_enable_cmdline_mode` | Enable ':' and ex commands. | `boolean` | `true`
`vintageous_hlsearch` | Highlight searches in '/', '?', etc. | `boolean` | `true`
`vintageous_ignorecase` | Ignore case in '/', '?', '*', and '#'. | `boolean` | `true`
`vintageous_incsearch` | Apply search patterns incrementally as they are typed. | `boolean` | `true`
`vintageous_log_level` | Logging level e.g 'debug', 'info', 'error', 'critical'. | `string` | `error`
`vintageous_magic` | Use regular expressions in '/' and '?' otherwise uses smart case, interpret pattern literally, and ignore case. | `boolean` | `true`
`vintageous_reset_mode_when_switching_tabs` | Reset to normal mode when a tab is activated. | `boolean` | `true`
`vintageous_use_ctrl_keys` | Enable key bindings prefaced by the CTRL modifier. | `boolean` | `false`
`vintageous_use_sys_clipboard` | Propagate copy actions to the system clipboard. | `boolean` | `false`
`vintageous_verbose` | Enable verbose logging. | `boolean` | `false`
`vintageous_visualbell` | Enable visual bell. | `boolean` | `true`
`vintageous_visualyank` | Enable visual bell when yanking. | `boolean` | `true`

## INSTALLATION

### Package Control installation

**Currently not available on Package Control. It will be soon once a new name is settled on.** The preferred method of installation will be [Package Control](https://packagecontrol.io/browse/authors/gerardroche).

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`Vintageous`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/gerardroche/Vintageous.git ~/.config/sublime-text-3/Packages/Vintageous`
    * OS X: `git clone https://github.com/gerardroche/Vintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/Vintageous`
    * Windows: `git clone https://github.com/gerardroche/Vintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/Vintageous`
3. Done!

## CONTRIBUTING

Your issue reports and pull requests are welcome.

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "Vintageous" as the package to test.

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

This project is a fork of [guillermooo/Vintageous](https://github.com/guillermooo/Vintageous).

## LICENSE

Released under the [MIT License](LICENSE).
