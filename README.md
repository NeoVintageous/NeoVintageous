# NeoVintageous

[![Build Status](https://travis-ci.org/NeoVintageous/NeoVintageous.svg?branch=master)](https://travis-ci.org/NeoVintageous/NeoVintageous) [![Build status](https://ci.appveyor.com/api/projects/status/g4pkv4ws1k2r1xna/branch/master?svg=true)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Latest Stable Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?style=flat-square&label=packagecontrol)](https://github.com/NeoVintageous/NeoVintageous/tags)

A Vim emulation layer for Sublime Text.

**This is a fork of Vintageous and is under active development. It will be published on Package Control in the next week or so.**

## OVERVIEW

* [Documentation](#documentation)
* [Configuration](#configuration)
* [Installation](#installation)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## DOCUMENTATION

See the [Neovim user documentation](https://neovim.io/doc/user).

Command | Description | Documentation | Dependencies | Notes
------- | ----------- | ------------- | ------------ | -----
ctrl-w, H | Move the current window to be at the very top | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_H) | | Only works in 2 col/row layouts
ctrl-w, J | Move the current window to be at the very bottom | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_J) | | Only works in 2 col/row layouts
ctrl-w, K | Move the current view to be at the far left | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_K) | | Only works in 2 col/row layouts
ctrl-w, L | Move the current window to be at the far right | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_L) | | Only works in 2 col/row layouts
ctrl-w, s | Split current window in two | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami)
ctrl-w, v | Split current window in two (vertically) | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami)

### Command Palette

Command | Description
------- | -----------
NeoVintageous: Reset |
NeoVintageous: Toggle Use Ctrl Keys |
NeoVintageous: Exit from Command Mode |
NeoVintageous: Open My .vintageousrc |
NeoVintageous: Open Changelog |
NeoVintageous: Open Readme |

## CONFIGURATION

Key | Description | Type | Default
----|-------------|------|--------
`vintageous_autoindent` | Enable auto indentation. | `boolean` | `true`
`vintageous_enable_cmdline_mode` | Enable ':' and ex commands. | `boolean` | `true`
`vintageous_enable_surround` | Enable surround.vim plugin. Provides mappings to easily delete, change and add such surroundings in pairs e.g. "cs", "ds", and "ys" actions. | `boolean` | `true`
`vintageous_hlsearch` | Highlight searches in '/', '?', etc. | `boolean` | `true`
`vintageous_ignorecase` | Ignore case in '/', '?', '*', and '#'. | `boolean` | `true`
`vintageous_incsearch` | Apply search patterns incrementally as they are typed. | `boolean` | `true`
`vintageous_magic` | Use regular expressions in '/' and '?' otherwise uses smart case, interpret pattern literally, and ignore case. | `boolean` | `true`
`vintageous_reset_mode_when_switching_tabs` | Reset to normal mode when a tab is activated. | `boolean` | `true`
`vintageous_surround_spaces` | Enable surround.vim plugin pair opener spaces, otherwise the pair closes have spaces i.e. if true then `ysw(` and `ysw)` -&gt; `( things )` and `(things)`, otherwise if false then `ysw(` and `ysw)` -&gt; `(things) and `( things )` | `boolean` | `false`
`vintageous_use_ctrl_keys` | Enable key bindings prefaced by the CTRL modifier. | `boolean` | `false`
`vintageous_use_sys_clipboard` | Propagate copy actions to the system clipboard. | `boolean` | `false`
`vintageous_visualbell` | Enable visual bell. | `boolean` | `true`
`vintageous_visualyank` | Enable visual bell when yanking. | `boolean` | `true`

### Use ctrl keys

To enable ctrl modifier keys set it globally: `Preferences > Settings`

```json
{
    "vintageous_use_ctrl_keys": true
}
```

Or set it per-project: `Project > Edit Project`

```json
{
    "settings": {
        "vintageous_use_ctrl_keys": true
    }
}
```

## INSTALLATION

### Package Control installation

**Currently not available on Package Control. It will be soon.** The preferred method of installation will be [Package Control](https://packagecontrol.io/browse/authors/NeoVintageous).

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`NeoVintageous`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`
    * OS X: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`
    * Windows: `git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`
3. Done!

## CONTRIBUTING

Your issue reports and pull requests are welcome.

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "NeoVintageous" as the package to test.

### Debugging

Logs are located in `Packages/.log/NeoVintageous.log`. The log level can be changed with a file in `Packages/.log/NeoVintageous` with the contents of the log level i.e. DEBUG, INFO, WARNING, ERROR, or CRITICAL.

### Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

For Linux and OSX [this script](httsp://github.com/gerardroche/dotfiles/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Check back soon for a Windows compatible script.

*Note: cleaning and reverting are two different tasks. Reverting will remove installed packages and configurations, cleaning will only remove files generated by Sublime Text at runtime like caches, indexes, workspaces, sessions, etc.*

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

This project is a fork of [guillermooo/Vintageous](https://github.com/guillermooo/Vintageous).

## LICENSE

Released under the [MIT License](LICENSE).
