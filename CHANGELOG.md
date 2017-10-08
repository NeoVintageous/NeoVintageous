# NEOVINTAGEOUS CHANGELOG

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## Unreleased

### Added

* Added: Support for `:UserCommand<CR>` `.vintageousrc` mappings
* Added: Support for `:excommand<CR>` `.vintageousrc` mappings
* Added: `:snoremap` command
* Added: `:smap` command
* Added: `cot` toggle sidebar command (Unimpaired plugin)
* Added: `[ot` toggle sidebar on command (Unimpaired plugin)
* Added: `]ot` toggle sidebar off command (Unimpaired plugin)
* Added: `com` toggle minimap command (Unimpaired plugin)
* Added: `[om` toggle minimap on command (Unimpaired plugin)
* Added: `]om` toggle minimap off command (Unimpaired plugin)
* Added: How to map `jk` to `Esc` (documentation)

### Changed

* Changed: Modeline `vintageous_modeline` is now disabled by default
* Changed: "Open Readme" command caption changed to "Readme"
* Changed: "Open Changelog" command caption changed to "Changelog"

### Removed

* Removed: Unimplemented `tabopen` ex command
* Removed: Deprecated `neovintageous_toggle_use_ctrl_keys` command
* Removed: Deprecated `neovintageous_reset` command
* Removed: Deprecated `neovintageous_exit_from_command_mode` command
* Removed: Deprecated `toggle_mode` command

### Fixed

* Fixed: Several `.vintageousrc` syntax highlighting bugs
* Fixed: Lots of Command-line mode syntax highlighting bugs

## 1.3.1 - 2017-07-31

* Fixed [#281](https://github.com/NeoVintageous/NeoVintageous/issues/281): `aW` text objects error if cursor starts at whitespace
* Fixed [#123](https://github.com/NeoVintageous/NeoVintageous/issues/123): text object `a<` or `i<` doesn't work!
* Fixed [#280](https://github.com/NeoVintageous/NeoVintageous/issues/280): `daW` / etc sometimes hang forever in LaTeX syntax
* Fixed: Handle upgrades and loading errors gracefully

## 1.3.0 - 2017-07-21

### Added

* Added [#271](https://github.com/NeoVintageous/NeoVintageous/issues/271): `ctrl+w q` should close window if closing the last view
* Added [#269](https://github.com/NeoVintageous/NeoVintageous/issues/269): `:close` ex command
* Added: `.vintageousrc` `<leader>` special string can be used more than once in a mapping e.g. `nnoremap <leader><leader> ggvG`
* Added: `.vintageousrc` `<leader>` special string can be used anywhere in mapping e.g. `nnoremap g<leader> ggvG`
* Added: `.vintageousrc` `noremap`, `nnoremap`, `vnoremap`, and `onoremap` commands
* Added: `.vintageousrc` syntax highlighting
* Added: `ctrl+n` and `ctrl+p` auto-complete navigation

  Command | Description
  ------- | -----------
  `ctrl+n` or `ctrl+j` | down
  `ctrl+p` or `ctrl+k` | up

* Added: `ctrl+n` and `ctrl+p` overlay navigation

  Command | Description | Notes
  ------- | ----------- | -----
  `ctrl+n` | down | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays
  `ctrl+p` | up | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays

* Added: Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) go to error commands

  Command | Description | Documentation | Dependencies
  ------- | ----------- | ------------- | ------------
  `[l` | Jump to `[count]` next error. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | [Linter](https://github.com/SublimeLinter/SublimeLinter3)
  `]l` | Jump to `[count]` previous error.. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | [Linter](https://github.com/SublimeLinter/SublimeLinter3)

* Added: Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) option toggling commands

  On | Off | Toggle | Description | Documentation
  -- | --- | ------ | ----------- | -------------
  `[oc` | `]oc` | `coc` | ['cursorline'](https://neovim.io/doc/user/options.html#%27cursorline%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ol` | `]ol` | `col` | ['list'](https://neovim.io/doc/user/options.html#%27list%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[on` | `]on` | `con` | ['number'](https://neovim.io/doc/user/options.html#%27number%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[os` | `]os` | `cos` | ['spell'](https://neovim.io/doc/user/options.html#%27spell%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ow` | `]ow` | `cow` | ['wrap'](https://neovim.io/doc/user/options.html#%27wrap%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)

* Added: Port of [abolish.vim](https://github.com/tpope/vim-abolish) coercion commands

  Command | Description | Documentation
  ------- | ----------- | -------------
  `crm` | Coerce word under cursor to MixedCase. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crc` | Coerce word under cursor to camelCase. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crs` | Coerce word under cursor to snake_case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr_` | Coerce word under cursor to snake_case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cru` | Coerce word under cursor to SNAKE_UPPERCASE. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crU` | Coerce word under cursor to SNAKE_UPPERCASE. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr-` | Coerce word under cursor to dash-case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crk` | Coerce word under cursor to kebab-case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr.` | Coerce word under cursor to dot.case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `cr<Space>` | Coerce word under cursor to space case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)
  `crt` | Coerce word under cursor to Title Case. | [abolish.vim](https://github.com/tpope/vim-abolish/blob/master/doc/abolish.txt)

* Added: How to map `jj` to `Esc` (documentation)
* Added: How to disable arrow keys (documentation)
* Added: Commentary plugin usage (documentation)
* Added: Surround plugin usage (documentation)

### Fixed

* Fixed: Command-line syntax `:quit` highlighting
* Fixed: Edge-case plugin conflict issues
* Fixed: Edge-case Unimpaired plugin issue adding blanks
* Fixed: Edge-case issue invalidating ex mode completions

## 1.2.0 - 2017-06-21

### Added

* Added [#252](https://github.com/NeoVintageous/NeoVintageous/issues/252): The package is now available in Package Control
* Added: Git diff commands

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `[c` | Jump backwards to the previous start of a change. | [diff](https://neovim.io/doc/user/diff.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)
  `]c` | Jump forwards to the next start of a change. | [diff](https://neovim.io/doc/user/diff.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)

* Added: Port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) is provided by default. *The implementation may not be complete. Please open issues about missing features.* *Below is a table of what is currently available.*

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `[<Space>` | Add `[count]` blank lines before the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `]<Space>` | Add `[count]` blank lines after the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `[e` | Exchange the current line with `[count]` lines above it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |
  `]e` | Exchange the current line with `[count]` lines below it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt) | |

* Added [#275](https://github.com/NeoVintageous/NeoVintageous/issues/275): Commands in the `.vintageousrc` file don't need to be prefixed with `:` (colon)
* Added [#187](https://github.com/NeoVintageous/NeoVintageous/issues/187): Switching to specific tab with `[count]` `gt`
* Added: `[count]` to `ctrl+e` and `ctrl+y` (scroll lines)
* Added: Coveralls code coverage reporting
* Added: Surround plugin usage (documentation)
* Added: `.vintageousrc` usage (documentation)
* Added: Modeline usage (documentation)
* Added: Multiple cursor usage (documentation)
* Added: Sidebar and Overlay navigation usage (documentation)

## 1.1.2 - 2017-06-05

### Fixed

* Fixed: `gt` command should wrap around from the last tab to the first tab
* Fixed: Command-line mode history edge-case error when no history available
* Fixed: Command-line mode history not working (regression)
* Fixed [#192](https://github.com/NeoVintageous/NeoVintageous/issues/192): Closing last tab shouldn’t close sublime window with project (documentation)
* Fixed [#122](https://github.com/NeoVintageous/NeoVintageous/issues/122): `Tab` doesn't work in visual mode (`Shift+Tab` does) (documentation)

## 1.1.1 - 2017-05-31

### Fixed

* Fixed: [#266](https://github.com/NeoVintageous/NeoVintageous/issues/266) `:nmap` doesn't work in `.vintageousrc` file
* Fixed: `:omap` doesn't work in `.vintageousrc` file
* Fixed: `:vmap` doesn't work in `.vintageousrc` file
* Fixed: `:set` prints debug messages to console even when debugging is disabled
* Fixed [#268](https://github.com/NeoVintageous/NeoVintageous/issues/268): `:set` doesn't work in some cases e.g. `:set hlsearch`
* Fixed: `:file` (`ctrl+g`) file name should be quoted
* Fixed: Readme link to Linux and OSX cleaner script is broken
* Fixed [#267](https://github.com/NeoVintageous/NeoVintageous/issues/267): Settings – User `.vintageousrc` menu item is broken
* Fixed [#169](https://github.com/NeoVintageous/NeoVintageous/issues/169): How to map this using Vintageous? (documentation)

## 1.1.0 - 2017-05-28

### Added

* Added: [ToggleNeoVintageous](https://github.com/NeoVintageous/ToggleNeoVintageous); A command to toggle NeoVintageous
* Added: Reload My `.vintageousrc` File command
* Added [#63](https://github.com/NeoVintageous/NeoVintageous/issues/63): `/` search does not highlight well
* Added: New commands

  Key | Context | Description
  --- | ------- | -----------
  `j` | Sidebar | down
  `k` | Sidebar | up
  `h` | Sidebar | close node / go to parent node
  `l` | Sidebar | open node
  `ctrl+j` | Overlay | down
  `ctrl+k` | Overlay | up
  `ctrl+[` | Normal | Same as `Esc` ([#249](https://github.com/NeoVintageous/NeoVintageous/issues/249))

### Fixed

* Fixed: Error when reloading and upgrading NeoVintageous and NeoVintageous plugins
* Fixed [#119](https://github.com/NeoVintageous/NeoVintageous/issues/119): Loosing user settings when toggling ctrl keys
* Fixed [#84](https://github.com/NeoVintageous/NeoVintageous/issues/84): More detail or examples for mapping
* Fixed [#34](https://github.com/NeoVintageous/NeoVintageous/issues/34): Small note regarding wiki OSX note
* Fixed [#162](https://github.com/NeoVintageous/NeoVintageous/issues/162): Use `sublime.packages_path()`
* Fixed [#246](https://github.com/NeoVintageous/NeoVintageous/issues/246): Error when toggling vintageous
* Fixed: `:!{cmd}` error (Windows)
* Fixed: `:!!` error (Windows)
* Fixed: `:new` error
* Fixed: `:edit` error
* Fixed: `:exit` error
* Fixed: `:wq!` error
* Fixed: `:wq` error

## 1.0.1 - 2017-04-28

### Fixed

* Fixed: `gq` error
* Fixed: error using registers
* Fixed: error when searching
* Fixed: running last ex command `!!` not working

## 1.0.0 - 2017-04-22

### Added

* Added: New commands

  Command | Description | Documentation | Dependencies | Notes
  ------- | ----------- | ------------- | ------------ | -----
  `ctrl+]` | Jump to the definition of the keyword under the cursor | [tagsearch](https://neovim.io/doc/user/tagsrch.html#CTRL-\]) | |
  `ctrl-w h` | Move cursor to view left of current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_h) | |
  `ctrl-w j` | Move cursor to view below current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_j) | |
  `ctrl-w k` | Move cursor to view above current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_k) | |
  `ctrl-w l` | Move cursor to view right of current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_l) | |
  `ctrl-w b` | Move cursor to bottom-right view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_b) | |
  `ctrl-w t` | Move cursor to top-left view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_t) | |
  `ctrl-w H` | Move the current window to be at the very top | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_H) | | Only works in 2-col or 2-row layouts
  `ctrl-w =` | Make all views (almost) equally high and wide | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_=) | |
  `ctrl-w _` | Set current view height as high as possible | [windows](https://neovim.io/doc/user/windows.html#CTRL-W__) | |
  `ctrl-w \|` | Set current view width as wide as possible | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_bar) | |
  `ctrl-w o` | Make the current view the only one on the screen | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_o) | |
  `ctrl-w c` | Close current view | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_c) | |
  `ctrl-w x` | Exchange current view with next one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_x) | |
  `ctrl-w s` | Split current window in two | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w v` | Split current window in two (vertically) | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w J` | Move the current window to be at the very bottom | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_J) | | Only works in 2-col or 2-row layouts
  `ctrl-w K` | Move the current view to be at the far left | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_K) | | Only works in 2-col or 2-row layouts
  `ctrl-w L` | Move the current window to be at the far right | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_L) | | Only works in 2-col or 2-row layouts
  `ctrl-w n` | Create new view below current one | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_n) | |
  `ga` | Print the ascii value of the character under the cursor in dec, hex and oct | [various](https://neovim.io/doc/user/various.html#ga) | |
  `ctrl+c` | Exit select mode | |
  `ctrl+[` | Exit select mode | |

* Added: Port of [surround.vim](https://github.com/tpope/vim-surround) is provided by default. It is based on the [Vintageous_Plugin_Surround](https://github.com/guillermooo/Vintageous_Plugin_Surround) plugin by @guillermooo
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
* Fixed: `CTRL-W_H` and `CTRL-W-L` windowing commands
* Fixed: Error raised trying to scroll in a transient view
* Fixed: `Esc` closes console even if already in normal mode and have a multiple selection
* Fixed: Console automatically closes on start
* Fixed: Wrong file permissions
* Fixed: `c_` and `d_` cause errors
* Fixed [#1042](https://github.com/guillermooo/Vintageous/pull/1042): Interactive commands not working after mapped commands
* Fixed [#1074](https://github.com/guillermooo/Vintageous/pull/1074): New text objects
* Fixed: Command-line mode syntax should not be listed in syntax menus
