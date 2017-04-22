# CHANGELOG

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## Unreleased

### Fixed

* Fixed: edge case error when searching
* Fixed: run last ex command "!!" not working

## 1.0.0 - 2017-04-22

### Added

* Added: New commands

    Command | Description | Documentation | Notes
    ------- | ----------- | ------------- | -----
    ctrl-w, ] | Jump to the definition of the keyword under the cursor | [Neovim doc](https://neovim.io/doc/user/tagsrch.html#CTRL-\]) |
    ctrl-w, h | Move cursor to view left of current one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_h) |
    ctrl-w, j | Move cursor to view below current one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_j) |
    ctrl-w, k | Move cursor to view above current one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_k) |
    ctrl-w, l | Move cursor to view right of current one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_l) |
    ctrl-w, b | Move cursor to bottom-right view | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_b) |
    ctrl-w, t | Move cursor to top-left view | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_t) |
    ctrl-w, H | Move the current window to be at the very top | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_H) | Currently only works in 2-col or 2-row layouts
    ctrl-w, = | Make all views (almost) equally high and wide | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_=) |
    ctrl-w, _ | Set current view height as high as possible | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W__) |
    ctrl-w, &vert; | Set current view width as wide as possible | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_bar) |
    ctrl-w, o | Make the current view the only one on the screen | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_o) |
    ctrl-w, c | Close current view | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_c) |
    ctrl-w, x | Exchange current view with next one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_x) |
    ctrl-w, s | Split current window in two | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_s) | Requires [Origami](https://github.com/SublimeText/Origami)
    ctrl-w, v | Split current window in two (vertically) | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_v) | Requires [Origami](https://github.com/SublimeText/Origami)
    ctrl-w, J | Move the current window to be at the very bottom | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_J) | Currently only works in 2-col or 2-row layouts
    ctrl-w, K | Move the current view to be at the far left | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_K) | Currently only works in 2-col or 2-row layouts
    ctrl-w, L | Move the current window to be at the far right | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_L) | Currently only works in 2-col or 2-row layouts
    ctrl-w, n | Create new view below current one | [Neovim doc](https://neovim.io/doc/user/windows.html#CTRL-W_n) |
    ga | Print the ascii value of the character under the cursor in dec, hex and oct | [Neovim doc](https://neovim.io/doc/user/various.html#ga) |

* Added: Allow `<C-c>` and `<C-[>` to exit select mode
* Added: `vi_search.comment` scope on search matches for better control of highlighting
* Added: `vintageous_visualyank` setting to disable visual bells when yanking text
* Added: The [surround.vim](https://github.com/guillermooo/Vintageous_Plugin_Surround) plugin by @guillermooo has been integrated and is enabled by default
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
