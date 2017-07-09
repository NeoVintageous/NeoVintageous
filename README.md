# NeoVintageous

[![Build Status](https://img.shields.io/travis/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://travis-ci.org/NeoVintageous/NeoVintageous) [![Build status](https://img.shields.io/appveyor/ci/gerardroche/neovintageous/master.svg?style=flat-square)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Coverage Status](https://img.shields.io/coveralls/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://coveralls.io/github/NeoVintageous/NeoVintageous?branch=master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?style=flat-square&label=stable)](https://github.com/NeoVintageous/NeoVintageous/tags) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Downloads](https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous)

Vintageous-fork, a Vim emulation layer for Sublime Text.

## OVERVIEW

* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [Contributing](#contributing)
* [Changelog](#changelog)
* [Credits](#credits)
* [License](#license)

## INSTALLATION

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/browse/authors/NeoVintageous).

### Manual installation

1. Close Sublime Text.
2. Download or clone this repository to a directory named **`NeoVintageous`** in the Sublime Text Packages directory for your platform:
    * Linux: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`
    * OS X: `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`
    * Windows: `git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`
3. Done!

## USAGE

What follows is supplementary documentation about Vim and Sublime Text feature differences. See the [Vim main help file](https://neovim.io/doc/user) for a complete guide on Vim.

Command | Description | Documentation | Dependencies | Notes
------- | ----------- | ------------- | ------------ | -----
`[c` | Jump backwards to the previous start of a change. | [diff](https://neovim.io/doc/user/diff.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)
`]c` | Jump forwards to the next start of a change. | [diff](https://neovim.io/doc/user/diff.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) | Disable wrapping: set `git_gutter_next_prev_change_wrap` to `false` (Preferences &gt; Settings)
`ctrl-w H` | Move the current window to be at the very top | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_H) | | Only works in 2 col/row layouts
`ctrl-w J` | Move the current window to be at the very bottom | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_J) | | Only works in 2 col/row layouts
`ctrl-w K` | Move the current view to be at the far left | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_K) | | Only works in 2 col/row layouts
`ctrl-w L` | Move the current window to be at the far right | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_L) | | Only works in 2 col/row layouts
`ctrl-w s` | Split current window in two | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami)
`ctrl-w v` | Split current window in two (vertically) | [windows](https://neovim.io/doc/user/windows.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami)

Command | Context | Description | Notes
------- | ------- | ----------- | -----
`j` | sidebar | down | `ctrl+0` focuses the sidebar
`k` | sidebar | up | `ctrl+0` focuses the sidebar
`h` | sidebar | close node / go to parent node | `ctrl+0` focuses the sidebar
`l` | sidebar | open node | `ctrl+0` focuses the sidebar
`ctrl+j` | overlay | down | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays
`ctrl+k` | overlay |up | e.g. `ctrl+p` and `ctrl+shift+p` invoke overlays

### Command Palette

Command | Description
------- | -----------
NeoVintageous: Open My .vintageousrc File | Open the runtime configuration file for editing
NeoVintageous: Reload My .vintageousrc File | Reload the runtime configuration file
NeoVintageous: Open Changelog | Open the changelog in a view
NeoVintageous: Open Readme | Open the readme in a view
Preferences: NeoVintageous Settings – Default | Open the default settings
Preferences: NeoVintageous Settings – User | Open the settings file for editing

### Toggle command

Use the official [ToggleNeoVintageous](https://github.com/NeoVintageous/ToggleNeoVintageous) plugin which provides a command to toggle NeoVintageous.

### The .vintageousrc file

A feature comparative to the [`.vimrc`](https://neovim.io/doc/user/usr_05.html#05.1) file. The file is located at `Packages/User/.vintageousrc` and is read during startup. There is limited support, the following are supported in basic use-cases: `:let mapleader=`, `:map`, `:nmap`, `:omap`, and `:vmap`.

    " The character " (the double quote mark) starts a comment

    let mapleader=,

    " Enter command line mode using space
    nmap <space> :

    " Visually select all content using ,a
    nmap <leader>a ggvG

    " Sort with ,s in visual mode
    vmap <leader>s <F9>

    " Scroll viewport faster ctrl+e and ctrl+y
    nmap <C-e> 3<C-e>
    nmap <C-y> 3<C-y>

    " Scroll down using shift-enter
    nmap <S-cr> <C-d>

Read more about mappings and the .vimrc file in the [Vim main help file](https://neovim.io/doc/user/map.html).

### Modeline

A feature comparative to [Vim Modeline](https://neovim.io/doc/user/options.html#modeline). A number of lines at the beginning and end of the file are checked for "modelines", the modelines (settings) will be applied to the view when it's opened.

    # sublime: gutter false
    # sublime: translate_tab_to_spaces true
    # sublime: rulers [80, 120]
    # sublime: tab_size 4

Read more about modeline in the [Vim main help file](https://neovim.io/doc/user/options.html#modeline).

### Multiple cursors

There two ways to use multiple selections.

The first is to enter insert mode, `i`, then use `ctrl+d` to make multiple selections, press `Esc` to enter normal mode, from here you can use NeoVintageous normally e.g. `$` will jump the cursors to the end of line, `^` all cursors to the start of line, `v` enters all cursors into visual mode, `f{char}` makes all cursors visually select to `{char}`, etc.

The second way is enter select mode, a non-standard mode that is used for multiple selections. *This mode is not the same as select mode in Vim.*

Key Sequence | Command
------------ | -------
`gh` | Enter select mode (from normal or visual mode)
`j` | Add selection
`k` | Remove selection
`l` | Skip current selection
`A` | Select all instances
`i` | Enter visual mode (preserving selections)
`J` | Clear multiple selections and enter normal mode
`gH` | After a search with `/` or `?`, select all matches.

Once you've created visual selections in select mode, you must return to insert mode by pressing `i` in order to edit text. Once in insert mode, you can switch to normal mode, etc. If you press `Esc` while in select mode, you will return to normal mode, but multiple carets won't be destroyed. If you press `Esc` a second time, you will be left with one single caret in normal mode.

### Commentary plugin

A port of [commentary.vim](https://github.com/tpope/vim-commentary) is provided by default.

*The implementation may not be complete. Please open issues about missing features.* *Below is a table of what is currently available.*

Command | Description | Documentation
------- | ----------- | -------------
`gc{motion}` | Comment or uncomment lines that `{motion}` moves over. | [commentary.vim](https://github.com/tpope/vim-commentary/blob/master/doc/commentary.txt)
`gcc` | Comment or uncomment current line. | [commentary.vim](https://github.com/tpope/vim-commentary/blob/master/doc/commentary.txt)
`{Visual}gc` | Comment or uncomment the highlighted lines. | [commentary.vim](https://github.com/tpope/vim-commentary/blob/master/doc/commentary.txt)

Read more about commentary usage in the [help file](https://github.com/tpope/vim-commentary/blob/master/doc/commentary.txt).

### Surround plugin

A port of [surround.vim](https://github.com/tpope/vim-surround) is provided by default.

*The implementation may not be complete. Please open issues about missing features.* *Below is a table of what is currently available.*

Command | Description | Documentation
------- | ----------- | -------------
`ds` | Delete surroundings. | [surround.vim](https://github.com/tpope/vim-surround/blob/master/doc/surround.txt)
`cs` | Change surroundings. | [surround.vim](https://github.com/tpope/vim-surround/blob/master/doc/surround.txt)
`ys` | Yank surroundings. | [surround.vim](https://github.com/tpope/vim-surround/blob/master/doc/surround.txt)

Read more about surround.vim usage in the [help file](https://github.com/tpope/vim-surround/blob/master/doc/surround.txt).

### Unimpaired plugin

A port of [unimpaired.vim](https://github.com/tpope/vim-unimpaired) is provided by default.

*The implementation may not be complete. Please open issues about missing features.* *Below is a table of what is currently available.*

Command | Description | Documentation
------- | ----------- | -------------
`[<Space>` | Add `[count]` blank lines before the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
`]<Space>` | Add `[count]` blank lines after the cursor. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
`[e` | Exchange the current line with `[count]` lines above it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)
`]e` | Exchange the current line with `[count]` lines below it. | [unimpaired.vim](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt)

Read more about unimpaired usage in the [help file](https://github.com/tpope/vim-unimpaired/blob/master/doc/unimpaired.txt).

### Other plugins

Please open issues about vim plugins you would like to see implemented, or about plugins you are thinking of writing because we may be willing to add it to the plugin by default.

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

### Mapping CapsLock to Escape

NeoVintageous cannot remap the caps lock. This is an OS level configuration e.g. on Ubuntu Gnome you can configure the caps lock to escape at the terminal:

    gsettings set org.gnome.desktop.input-sources xkb-options "['caps:escape']"

### Holding down a key like j does not repeat the command

This is a feature of OS X Lion and newer versions.

To make a key repeat a command when holding it down, run this once at the terminal:

    defaults write com.sublimetext.3 ApplePressAndHoldEnabled -bool false

### Better search highlighting support

Color schemes can [support better search highlighting](https://github.com/NeoVintageous/NeoVintageous/issues/63#issuecomment-301948594) via the following scopes:

     <dict>
        <key>scope</key>
        <string>string.search</string>
        <key>settings</key>
        <dict>
            <key>foreground</key>
            <string>#000000</string>
            <key>background</key>
            <string>#C4BE89</string>
        </dict>
    </dict>
    <dict>
        <key>scope</key>
        <string>string.search.occurrence</string>
        <key>settings</key>
        <dict>
            <key>foreground</key>
            <string>#000000</string>
            <key>background</key>
            <string>#FFE792</string>
        </dict>
    </dict>

### Disabling arrow keys

Add as many of the following key bindings as you would like to disable.

```json
[
    {"keys": ["left"],              "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["right"],             "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["up"],                "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["down"],              "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["alt+left"],          "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["alt+down"],          "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["alt+up"],            "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["alt+right"],         "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+left"],         "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+down"],         "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+up"],           "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+right"],        "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+left"],   "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+down"],   "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+up"],     "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+right"],  "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+tab"],          "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+left"],   "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+down"],   "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+up"],     "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["ctrl+shift+right"],  "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["shift+left"],        "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["shift+down"],        "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["shift+up"],          "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]},
    {"keys": ["shift+right"],       "command": "null", "context": [{"key": "setting.neovintageous_disable_arrow_keys"}, {"key": "auto_complete_visible", "operand": false}, {"key": "overlay_visible", "operand": false}, {"key": "popup_visible", "operand": false}, {"key": "setting.is_widget", "operator": "equal", "operand": false}]}
]
```

Then enable them: `Preferences > Settings`

```json
{
    "neovintageous_disable_arrow_keys": true
}
```

## CONTRIBUTING

Your issue reports and pull requests are welcome.

### Tests

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press Enter and input "NeoVintageous" as the package to test.

### Debugging

The Sublime Text startup log can be read by going to `Menu > View > Show Console`.

Sublime Text command and input logging can be enabled in the console (run the commands in input box at the bottom of the console panel): `sublime.log_commands(True); sublime.log_input(True)`. Other logging such as regex results, indexing, and build systems can be enabled too: `sublime.log_result_regex(True); sublime.log_indexing(True); sublime.log_build_systems(True)`.

Neovintageous debug messages are disabled by default. To enable them set an environment variable named `SUBLIME_NEOVINTAGEOUS_DEBUG` to a non-blank value. See [Set a Sublime Text environment variable](https://github.com/gerardroche/sublime-phpunit#debugging) for a step by step guide on how to set an environment variable for Sublime Text. The debug message log is located at `Packages/User/NeoVintageous.log`. Debug messages are also printed to the console: `Menu > View > Show Console`.

### Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

For Linux and OSX [this script](https://github.com/gerardroche/dotfiles/blob/7f7812393e26db7c0f8146f5b6db730197dfd103/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Check back soon for a Windows compatible script.

*Note: cleaning and reverting are two different tasks. Reverting will remove installed packages and configurations, cleaning will only remove files generated by Sublime Text at runtime like caches, indexes, workspaces, sessions, etc.*

## CHANGELOG

See [CHANGELOG.md](CHANGELOG.md).

## CREDITS

This project is a fork of [Vintageous](https://github.com/guillermooo/Vintageous).

## LICENSE

Released under the [MIT License](LICENSE).
