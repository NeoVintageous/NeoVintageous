# NEOVINTAGEOUS CHANGELOG

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## Unreleased

### Added

* Added: New commands

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  [c | Jump backwards to the previous start of a change. | [diff](https://neovim.io/doc/user/diff.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) |
  ]c | Jump forwards to the next start of a change. | [diff](https://neovim.io/doc/user/diff.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) |

* Added: [count] to ctrl+e and ctrl+y (scroll lines)

## [1.1.2](https://github.com/NeoVintageous/NeoVintageous/releases/tag/1.1.1) - 2017-06-05

### Fixed

* Fixed: gt command should wrap around from the last tab to the first tab
* Fixed: Command-line mode history edge-case error when no history available
* Fixed: Command-line mode history not working (regression)
* Fixed [#192](https://github.com/NeoVintageous/NeoVintageous/issues/192): Closing last tab shouldn’t close sublime window with project (documentation)
* Fixed [#122](https://github.com/NeoVintageous/NeoVintageous/issues/122): Tab doesn't work in visual mode (Shift+Tab does) (documentation)

## [1.1.1](https://github.com/NeoVintageous/NeoVintageous/releases/tag/1.1.1) - 2017-05-31

### Fixed

* Fixed: [#266](https://github.com/NeoVintageous/NeoVintageous/issues/266) :nmap doesn't work in .vintageous file
* Fixed: :omap doesn't work in .vintageous file
* Fixed: :vmap doesn't work in .vintageous file
* Fixed: :set prints debug messages to console even when debugging is disabled
* Fixed [#268](https://github.com/NeoVintageous/NeoVintageous/issues/268): :set doesn't work in some cases e.g. :set hlsearch
* Fixed: :file (ctrl+g) file name should be quoted
* Fixed: Readme link to Linux and OSX cleaner script is broken
* Fixed [#267](https://github.com/NeoVintageous/NeoVintageous/issues/267): Settings – User .vintageousrc menu item is broken
* Fixed [#169](https://github.com/NeoVintageous/NeoVintageous/issues/169): How to map this using Vintageous?

## [1.1.0](https://github.com/NeoVintageous/NeoVintageous/releases/tag/1.1.0) - 2017-05-28

### Added

* Added: [ToggleNeoVintageous](https://github.com/NeoVintageous/ToggleNeoVintageous), A command to toggle NeoVintageous
* Added: Reload My `.vintageousrc` File command
* Added [#63](https://github.com/NeoVintageous/NeoVintageous/issues/63): "/" search does not highlight well
* Added: New commands

    Key | Context | Description
    --- | ------- | -----------
    <kbd>j</kbd> | Sidebar | down
    <kbd>k</kbd> | Sidebar | up
    <kbd>h</kbd> | Sidebar | close node / go to parent node
    <kbd>l</kbd> | Sidebar | open node
    <kbd>ctrl+j</kbd> | Overlay | down
    <kbd>ctrl+k</kbd> | Overlay | up
    <kbd>ctrl+[</kbd> | Normal | Same as <kbd>Esc</kbd> ([#249](https://github.com/NeoVintageous/NeoVintageous/issues/249))

### Fixed

* Fixed: Error when reloading and upgrading NeoVintagous and NeoVintageous plugins
* Fixed [#119](https://github.com/NeoVintageous/NeoVintageous/issues/119): Loosing user settings when toggling ctrl keys
* Fixed [#84](https://github.com/NeoVintageous/NeoVintageous/issues/84): More detail or examples for mapping
* Fixed [#34](https://github.com/NeoVintageous/NeoVintageous/issues/34): Small note regarding wiki OSX note
* Fixed [#162](https://github.com/NeoVintageous/NeoVintageous/issues/162): Use sublime.packages_path()
* Fixed [#246](https://github.com/NeoVintageous/NeoVintageous/issues/246): Error when toggling vintageous
* Fixed: :!{cmd} error (Windows)
* Fixed: :!! error (Windows)
* Fixed: :new error
* Fixed: :edit error
* Fixed: :exit error
* Fixed: :wq! error
* Fixed: :wq error

## [1.0.1](https://github.com/NeoVintageous/NeoVintageous/releases/tag/1.0.1) - 2017-04-28

### Fixed

* Fixed: `gq` error
* Fixed: error using registers
* Fixed: error when searching
* Fixed: running last ex command "!!" not working

## [1.0.0](https://github.com/NeoVintageous/NeoVintageous/releases/tag/1.0.0) - 2017-04-22

### Added

* Added: New commands

    Command | Description | Documentation | Dependencies | Notes
    ------- | ----------- | ------------- | ------------ | -----
    ctrl-w, ] | Jump to the definition of the keyword under the cursor | [tagsearch](https://neovim.io/doc/user/tagsrch.html#CTRL-\]) | |
    ctrl-w, h | Move cursor to view left of current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_h) | |
    ctrl-w, j | Move cursor to view below current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_j) | |
    ctrl-w, k | Move cursor to view above current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_k) | |
    ctrl-w, l | Move cursor to view right of current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_l) | |
    ctrl-w, b | Move cursor to bottom-right view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_b) | |
    ctrl-w, t | Move cursor to top-left view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_t) | |
    ctrl-w, H | Move the current window to be at the very top | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_H) | | Only works in 2-col or 2-row layouts
    ctrl-w, = | Make all views (almost) equally high and wide | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_=) | |
    ctrl-w, _ | Set current view height as high as possible | [windows](https://neovim.io/doc/user/windows.html#CTRL-W__) | |
    ctrl-w, &vert; | Set current view width as wide as possible | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_bar) | |
    ctrl-w, o | Make the current view the only one on the screen | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_o) | |
    ctrl-w, c | Close current view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_c) | |
    ctrl-w, x | Exchange current view with next one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_x) | |
    ctrl-w, s | Split current window in two | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami) |
    ctrl-w, v | Split current window in two (vertically) | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami) |
    ctrl-w, J | Move the current window to be at the very bottom | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_J) | | Only works in 2-col or 2-row layouts
    ctrl-w, K | Move the current view to be at the far left | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_K) | | Only works in 2-col or 2-row layouts
    ctrl-w, L | Move the current window to be at the far right | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_L) | | Only works in 2-col or 2-row layouts
    ctrl-w, n | Create new view below current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_n) | |
    ga | Print the ascii value of the character under the cursor in dec, hex and oct | [various](https://neovim.io/doc/user/various.html#ga) | |
    ctrl+c | Exit select mode | |
    ctrl+[ | Exit select mode | |

* Added: Port of [tpope/vim-surround](https://github.com/tpope/vim-surround) based on the [Vintageous_Plugin_Surround](https://github.com/guillermooo/Vintageous_Plugin_Surround) plugin by @guillermooo
* Added: `vi_search.comment` scope on search matches for better control of highlighting
* Added: `vintageous_visualyank` setting to disable visual bells when yanking text
* Added [#1077](https://github.com/guillermooo/Vintageous/pull/1077): Support for Sublime Wrap Plus
* Added: Command-line mode syntax uses new syntax format
* Added: Open README and Open CHANGELOG command palette commands
* Added: Package Control menus for opening README, CHANGELOG, and LICENSE

### Removed

* Removed: Settings

    Setting | Description | Notes
    ------- | ----------- | -----
    `vintageous_test_runner_keymaps` | Enable test runner keymaps | Tests are now run using [UnitTesting](https://github.com/randy3k/UnitTesting)
    `vintageous_log_level` | | No longer used for logging
    `vintageous_verbose` | | No longer used for logging

### Fixed

* Fixed: Double loading and unnecessary loading, unloading, and loading of modules on start
* Fixed: Logging messages printed multiple times
* Fixed: CTRL-W_H and CTRL-W-L windowing commands
* Fixed: Error raised trying to scroll in a transient view
* Fixed: Esc closes console even if already in normal mode and have a multiple selection
* Fixed: Console automatically closes on start
* Fixed: Wrong file permissions
* Fixed: `c_` and `d_` cause errors
* Fixed [#1042](https://github.com/guillermooo/Vintageous/pull/1042): Interactive commands not working after mapped commands
* Fixed [#1074](https://github.com/guillermooo/Vintageous/pull/1074): New text objects
* Fixed: Command-line mode syntax should not be listed in syntax menus
