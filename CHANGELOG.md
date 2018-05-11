# NEOVINTAGEOUS CHANGELOG

All notable changes are documented in this file using the [Keep a CHANGELOG](http://keepachangelog.com/) principles.

## Unreleased (1.6.0)

## Added

* Added [#312](https://github.com/NeoVintageous/NeoVintageous/issues/312): Map commands with arguments e.g. `nnoremap ,f :ShowOverlay overlay=goto text=@<CR>`, `nnoremap ,p :ShowOverlay overlay=goto show_files=true<CR>`
* Added [#345](https://github.com/NeoVintageous/NeoVintageous/issues/345): Map commands without executing e.g `nnoremap ,r :reg`
* Added [#346](https://github.com/NeoVintageous/NeoVintageous/issues/346): Map commands with ranges and counts
* Added [#344](https://github.com/NeoVintageous/NeoVintageous/issues/344): Add buffer commands `:bf[irst]`, `:br[ewind]`, `:bp[revious]`, `:bN[ex]t`, `:bn[ext]`, and `:bl[ast]`
* Added [#343](https://github.com/NeoVintageous/NeoVintageous/issues/343): Add Unimpaired `[b`, `]b`, `[B`, `]B`, `]t`, `[t`, `]T`, and `[T`
* Added [#327](https://github.com/NeoVintageous/NeoVintageous/issues/327): Redo command (`<C-r>`) should invoke a UI bell if no more redo commands
* Added [#70](https://github.com/NeoVintageous/NeoVintageous/issues/70): `:set list` should show whitespace
* Added [#334](https://github.com/NeoVintageous/NeoVintageous/issues/334): Implement `:tabN[ext]` (`:tabprevious` alias)
* Added [#330](https://github.com/NeoVintageous/NeoVintageous/issues/330): Implement `:tabc[lose]`

## Fixed

* Fixed [#350](https://github.com/NeoVintageous/NeoVintageous/issues/350): Multi-select `k` doesn't work with a count
* Fixed [#314](https://github.com/NeoVintageous/NeoVintageous/issues/314): `gj` and `gk` do not work in visual line mode
* Fixed [#341](https://github.com/NeoVintageous/NeoVintageous/issues/341): Multi-select should scroll viewport to end of selection
* Fixed [#273](https://github.com/NeoVintageous/NeoVintageous/issues/273): Sort Lines command sorts whole file
* Fixed [#338](https://github.com/NeoVintageous/NeoVintageous/issues/338): `gv` after visual line should be linewise
* Fixed [#349](https://github.com/NeoVintageous/NeoVintageous/issues/349): `>` and `<` should leave cursor on first non whitespace character
* Fixed [#348](https://github.com/NeoVintageous/NeoVintageous/issues/348): `gv` doesn't remember which visual mode was last used
* Fixed [#347](https://github.com/NeoVintageous/NeoVintageous/issues/347): `gv` doesn't work in visual mode
* Fixed [#336](https://github.com/NeoVintageous/NeoVintageous/issues/336): `*` and `#` should center match on screen if not visible
* Fixed [#328](https://github.com/NeoVintageous/NeoVintageous/issues/328): Entering normal mode should not put cursor on EOL character
* Fixed [#324](https://github.com/NeoVintageous/NeoVintageous/issues/324): Entering Normal mode from Visual Block mode creates multiple selection
* Fixed [#329](https://github.com/NeoVintageous/NeoVintageous/issues/329): Redo command should not leave cursor on EOL character
* Fixed [#209](https://github.com/NeoVintageous/NeoVintageous/issues/209): Jumping to mark in visual mode does not work
* Fixed [#335](https://github.com/NeoVintageous/NeoVintageous/issues/335): Help subjects should be case sensitive e.g. `help L` should open help for L not l
* Fixed [#333](https://github.com/NeoVintageous/NeoVintageous/issues/333): `:ou` (`:ounmap` alias) doesn't work
* Fixed [#332](https://github.com/NeoVintageous/NeoVintageous/issues/332): `:no` (`:noremap` alias) doesn't work
* Fixed [#331](https://github.com/NeoVintageous/NeoVintageous/issues/331): `:files` doesn't work
* Fixed [#325](https://github.com/NeoVintageous/NeoVintageous/issues/325): `:sunmap` doesn't work, prints message E492: Not an editor command
* Fixed [#324](https://github.com/NeoVintageous/NeoVintageous/issues/324): Entering Normal mode from Visual Block mode creates multiple selection
* Fixed [#323](https://github.com/NeoVintageous/NeoVintageous/issues/323): `:g!/222/p` is bailing out with error: 'str' object has no attribute 'consume'
* Fixed [#153](https://github.com/NeoVintageous/NeoVintageous/issues/153): Cursor gets stuck after a few edit operations
* Fixed [#322](https://github.com/NeoVintageous/NeoVintageous/issues/322): `:print` doesn't work
* Fixed [#320](https://github.com/NeoVintageous/NeoVintageous/issues/320): `:move`  `KeyError: 'next_sel'` when address is the same as current line
* Fixed [#321](https://github.com/NeoVintageous/NeoVintageous/issues/321): Entering cmdline-mode from Visual Block mode doesn't work
* Fixed [#319](https://github.com/NeoVintageous/NeoVintageous/issues/319): `:cd` should change the current directory to the home directory
* Fixed [#150](https://github.com/NeoVintageous/NeoVintageous/issues/150): Remove lines with regular expression
* Fixed [#148](https://github.com/NeoVintageous/NeoVintageous/issues/148): `:$` does not go to last line
* Fixed [#87](https://github.com/NeoVintageous/NeoVintageous/issues/87): Double front slash doesn't escape properly

## Removed

* Removed: Deprecated SublimeLinter API calls

## 1.5.3 - 2018-03-24

### Fixed

* Fixed [#36](https://github.com/NeoVintageous/NeoVintageous/issues/36) `*` and `#` jump history doesn't work
* Fixed [#51](https://github.com/NeoVintageous/NeoVintageous/issues/51): Can't map umlauts
* Fixed [#144](https://github.com/NeoVintageous/NeoVintageous/issues/144): Can't repeat macros
* Fixed [#170](https://github.com/NeoVintageous/NeoVintageous/issues/170): `<` text object not finding the opening bracket correctly

## 1.5.2 - 2018-03-03

### Fixed

* Fixed: `:registers` should display `^J` to indicate newlines
* Fixed: `:registers` should truncate long lines
* Fixed: Add missing delete surround punctuation marks `;:@#~*\\/` e.g. `ds@`, `ds*`, etc.
* Fixed [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cst<{tagname}>`
* Fixed [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cstt{tagname}>` ("t" an alias for "<")
* Fixed [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cst{replacement}`
* Fixed [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cs{target}<{tagname}>`
* Fixed [#307](https://github.com/NeoVintageous/NeoVintageous/issues/307): Change surround tag `cs{target}t{tagname}>` ("t" is alias for "<")
* Fixed [#136](https://github.com/NeoVintageous/NeoVintageous/issues/136): Saving to named register with `D` doesn't work
* Fixed [#306](https://github.com/NeoVintageous/NeoVintageous/issues/306): Triple-clicking doesn't select a line

## 1.5.1 - 2018-02-20

### Fixed

* Fixed [#305](https://github.com/NeoVintageous/NeoVintageous/issues/305): Surround multiple selections leave cursor in wrong position
* Fixed: Edge-case infinite loop when special key is set with no default value
* Fixed [#304](https://github.com/NeoVintageous/NeoVintageous/issues/304): `:s/$/foo/gc` causes infinite loop
* Fixed [#210](https://github.com/NeoVintageous/NeoVintageous/issues/210): `:%s/$/,/` not working as expected
* Fixed: `:shell` error

## 1.5.0 - 2018-02-06

### Added

* Added: `:edit {file}` command
* Added [#288](https://github.com/NeoVintageous/NeoVintageous/issues/288): Command-line editing commands: `<C-b>`, `<C-e>`, `<C-h>`, `<C-n>`, `<C-p>`, `<C-u>`, and `<C-w>`
* Added [#279](https://github.com/NeoVintageous/NeoVintageous/issues/279): `CTRL-c` and `CTRL-[` should exit Command-line mode
* Added [#12](https://github.com/NeoVintageous/NeoVintageous/issues/12): Command-line search history with `/` and `?` (current session only)
* Added: Selections are now cleared when leaving a the current view (UX)
* Added: `NeovintageousToggleSideBar` command
* Added [#286](https://github.com/NeoVintageous/NeoVintageous/issues/286): Support for super-keys `<D-...>` (known as command-keys on OSX, and window-keys on Windows) (disabled by default)
* Added: `highlighted.yank` scope to highlighted yank regions to allow color scheme customisation
* Added: Switching windows using windowing commands no longer suddenly scrolls view (UX)
* Added: `:sunm[ap]` command
* Added: `:help {subject}` command now uses basic heuristics to find a relevant help topic if a subject is not found
* Added: Support for `'vintageous_modelines'` option (defaults to `5`)
* Added [#254](https://github.com/NeoVintageous/NeoVintageous/issues/254): `:sp[lit] [file]` command
* Added: Unimpaired status bar toggle `coe` (also toggle on `[oe`, and toggle off `]oe`)
* Added: Unimpaired menu toggle `coa` (also toggle on `[oa`, and toggle off `]oa`)
* Added: Support for the new SublimeLinter API using the Unimpaired goto to error commands `]l` and `[l`
* Added: Support for the new GitGutter API using the Unimpaired goto change commands `]c` and `[c`
* Added: `vintageousrc` (documentation)
* Added: Default vim options (documentation)

### Removed

* Removed: Recursive mappings commands `:map`, `:nmap`, `:omap`, `:smap`, `:vmap`. Use the non recursive commands instead.

  The recursive mappings were removed because they were not implemented as recursive mappings, and removing them now in preference of the non-recursive may prevent some potential problems in the future if the recursive mapping commands are ever implemented.

  Here is a table of the recursive, which have been removed, and the non recursive mapping commands that you can use instead:

  Recursive command | Non recursive command
  ----------------- | ---------------------
  `map` | `noremap`
  `nmap` | `nnoremap`
  `omap` | `onoremap`
  `smap` | `snoremap`
  `vmap` | `vnoremap`

* Removed: Unused `vintageous_enable_cmdline_mode` setting

### Fixed

* Fixed: Visual ex mode commands should enter normal mode after operation
* Fixed: Ex mode shell command error (Windows)
* Fixed: Unmap commands don't unmap visual mappings
* Fixed: Can't unmap mappings with special keys e.g. `<leader>`
* Fixed: Running tests shouldn't resets user vintageousrc mappings
* Fixed [#156](https://github.com/NeoVintageous/NeoVintageous/issues/156): `SHIFT-v` then `CTRL-b` doesn't work
* Fixed: Help views should be read only
* Fixed: Unknown registers raise an exception
* Fixed: `gc{motion}` leaves cursor at wrong place
* Fixed: `gcc` leaves cursor at wrong place
* Fixed: Repeat searches (`n`/`N`) should scroll and show surrounds
* Fixed: Goto next/prev change cursor position after motion (Unimpaired)
* Fixed [#285](https://github.com/NeoVintageous/NeoVintageous/issues/285): Page down `CTRL-f` does not work correctly in Visual Line mode
* Fixed [#296](https://github.com/NeoVintageous/NeoVintageous/issues/296): `de` leaves cursor at wrong place
* Fixed [#295](https://github.com/NeoVintageous/NeoVintageous/issues/295): `df{char}` leaves cursor at wrong place
* Fixed: `df$` leaves cursor at wrong place
* Fixed: `gq` cursor position after operation
* Fixed: Mapping command status messages
* Fixed: Error message typos and grammar
* Fixed [#254](https://github.com/NeoVintageous/NeoVintageous/issues/254): `:vs[plit] [file]` raises a TypeError

## 1.4.4 - 2018-01-07

* Fixed: Error trying to Open My Rc File first time
* Fixed: Help files shouldn't display rulers or indent guides
* Fixed: `CTRL-a` and `CTRL-x` doesn't work in column one or between lines
* Fixed: Update to latest vimdocs
* Fixed: `:map` doesn't work in visual block or visual line mode
* Fixed: Remove unused setting
* Fixed: Settings should be erased when cleaning up views
* Fixed: `gx` in quoted urls
* Fixed: `gg` and `G` jump history forwards `CTRL-i` and backwards `CTRL-o`
* Fixed [#298](https://github.com/NeoVintageous/NeoVintageous/issues/298): `gd` can't jump back with `CTRL-o`
* Fixed [#241](https://github.com/NeoVintageous/NeoVintageous/issues/241): Leaving Insert mode still shows as being in Insert mode
* Fixed [#129](https://github.com/NeoVintageous/NeoVintageous/issues/129): Failing tests when ST hasn't got focus

## 1.4.3 - 2017-12-22

### Fixed

* Fixed [#297](https://github.com/NeoVintageous/NeoVintageous/issues/297): An occurred trying load NeoVintageous

## 1.4.2 - 2017-12-19

### Fixed

* Fixed [#238](https://github.com/NeoVintageous/NeoVintageous/issues/238): Simply search & replace not working for me
* Fixed [#111](https://github.com/NeoVintageous/NeoVintageous/issues/111): Bad command
* Fixed: "Traling characters" Status message typo
* Fixed: `:s[ubstitute]` No previous substitute error message is incorrect
* Fixed: [#226](https://github.com/NeoVintageous/NeoVintageous/issues/226): Mouse does not reset cursor column
* Fixed: `C-w _` (set current group height as high as possible) doesn't always work correctly
* Fixed: `C-w |` (set current group width as wide as possible) doesn't always work correctly
* Fixed: `C-w =` (resize all groups equally) doesn't always work correctly
* Fixed: `gJ`
* Fixed: `gx` should ignore trailing full stops
* Fixed: `gx` doesn't work on markdown links
* Fixed: `vintageousrc` mapping should not accept unescaped pipe characters
* Fixed: Help syntax fixes
* Fixed: Unimpaired toggles (documentation)

## 1.4.1 - 2017-11-09

### Fixed

* Fixed [#245](https://github.com/NeoVintageous/NeoVintageous/issues/245): `ZZ` and `ZQ` are broken again
* Fixed [#290](https://github.com/NeoVintageous/NeoVintageous/issues/290): Commands that start with underscore should not be mappable
* Fixed [#289](https://github.com/NeoVintageous/NeoVintageous/issues/289): `:help {subject}` should goto `:{subject}` if `{subject}` not found

## 1.4.0 - 2017-11-06

### Added

* Added: `ds(`, `ds{`, `ds[`, and `ds<` now also trims contained whitespace (Surround plugin)
* Added: `dsb` alias for `ds)` delete surrounding `()` (Surround plugin)
* Added: `dsB` alias for `ds}` delete surrounding `{}` (Surround plugin)
* Added: `dsr` alias for `ds]` delete surrounding `[]` (Surround plugin)
* Added: `dsa` alias for `ds>` delete surrounding `<>` (Surround plugin)
* Added: `ds<` delete surrounding `<>` (Surround plugin)
* Added: `ds>` delete surrounding `<>` (Surround plugin)
* Added: `dst` delete surrounding pair of HTML or XML tags (Surround plugin)
* Added: `ds` followed by a target that is not one of the punctuation pairs, `()[]{}<>`, are now only searched for on the current line (Surround plugin)
* Added: `ds{target}` cursor position is now moves to the start of first target (Surround plugin)
* Added: `cs{target}` followed by one of `])}` now inserts an inner whitespace character (Surround plugin)
* Added: `cs>{replacement}` now replaces surround tag characters `<>` with replacement (Surround plugin)
* Added: `cs{target}` folowed by `>` now replaces target with replacement surroundings `<>` (Surround plugin)
* Added: `cs{target}{replacement}` cursor position is now moves to the start of first target (Surround plugin)
* Added: `:h[elp] {subject}` like ":help", additionally jump to the tag `{subject}`
* Added: `:h[elp]` open a view and display the help file
* Added: `gx` open url under cursor in browser
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
* Added: Documentation command
* Added: Edit Settings command
* Added: How to map `jk` to `Esc` (documentation)

### Changed

* Changed: `ds<` no longer deletes surrounding tag; use `dst` instead (Surround plugin)
* Changed: `ds>` no longer deletes surrounding tag; use `dst` instead (Surround plugin)
* Changed: Modeline `vintageous_modeline` is disabled by default
* Changed: "Open Changelog" command caption changed to "Changelog"

### Removed

* Removed: `vintageous_surround_spaces` setting
* Removed: Unimplemented `tabopen` ex command
* Removed: Deprecated `neovintageous_toggle_use_ctrl_keys` command
* Removed: Deprecated `neovintageous_reset` command
* Removed: Deprecated `neovintageous_exit_from_command_mode` command
* Removed: Deprecated `toggle_mode` command

### Fixed

* Fixed [#213](https://github.com/NeoVintageous/NeoVintageous/issues/213): No command accepts characters in a keybinding
* Fixed [#167](https://github.com/NeoVintageous/NeoVintageous/issues/167): Allow .vintageousrc to map any keybinds
* Fixed [#152](https://github.com/NeoVintageous/NeoVintageous/issues/152): `f<key>` doesn't jump to `<key>` if there is a mapping for `<key>`
* Fixed [#97](https://github.com/NeoVintageous/NeoVintageous/issues/97): Mapping commands
* Fixed [#81](https://github.com/NeoVintageous/NeoVintageous/issues/81): `ct<leader>` or `cf<leader>` doesn't work; need `ct<leader><leader>`
* Fixed [#282](https://github.com/NeoVintageous/NeoVintageous/issues/282): Surround doesn't work as expected on first symbol
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
  `[oc` | `]oc` | `coc` | ['cursorline'](https://vimhelp.appspot.com/options.txt.html#%27cursorline%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ol` | `]ol` | `col` | ['list'](https://vimhelp.appspot.com/options.txt.html#%27list%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[on` | `]on` | `con` | ['number'](https://vimhelp.appspot.com/options.txt.html#%27number%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[os` | `]os` | `cos` | ['spell'](https://vimhelp.appspot.com/options.txt.html#%27spell%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
  `[ow` | `]ow` | `cow` | ['wrap'](https://vimhelp.appspot.com/options.txt.html#%27wrap%27) | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)

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
  `[c` | Jump backwards to the previous start of a change. | [diff](https://vimhelp.appspot.com/diff.txt.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)
  `]c` | Jump forwards to the next start of a change. | [diff](https://vimhelp.appspot.com/diff.txt.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)

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
  `ctrl+]` | Jump to the definition of the keyword under the cursor | [tagsearch](https://vimhelp.appspot.com/tagsrch.txt.html#CTRL-\]) | |
  `ctrl-w h` | Move cursor to view left of current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_h) | |
  `ctrl-w j` | Move cursor to view below current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_j) | |
  `ctrl-w k` | Move cursor to view above current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_k) | |
  `ctrl-w l` | Move cursor to view right of current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_l) | |
  `ctrl-w b` | Move cursor to bottom-right view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_b) | |
  `ctrl-w t` | Move cursor to top-left view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_t) | |
  `ctrl-w H` | Move the current window to be at the very top | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_H) | | Only works in 2-col or 2-row layouts
  `ctrl-w =` | Make all views (almost) equally high and wide | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_=) | |
  `ctrl-w _` | Set current view height as high as possible | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W__) | |
  `ctrl-w \|` | Set current view width as wide as possible | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_bar) | |
  `ctrl-w o` | Make the current view the only one on the screen | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_o) | |
  `ctrl-w c` | Close current view | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_c) | |
  `ctrl-w x` | Exchange current view with next one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_x) | |
  `ctrl-w s` | Split current window in two | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w v` | Split current window in two (vertically) | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami) |
  `ctrl-w J` | Move the current window to be at the very bottom | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_J) | | Only works in 2-col or 2-row layouts
  `ctrl-w K` | Move the current view to be at the far left | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_K) | | Only works in 2-col or 2-row layouts
  `ctrl-w L` | Move the current window to be at the far right | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_L) | | Only works in 2-col or 2-row layouts
  `ctrl-w n` | Create new view below current one | [windows](https://vimhelp.appspot.com/windows.txt.html#CTRL-W_n) | |
  `ga` | Print the ascii value of the character under the cursor in dec, hex and oct | [various](https://vimhelp.appspot.com/various.txt.html#ga) | |
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
