# NeoVintageous

[![Build Status](https://travis-ci.org/NeoVintageous/NeoVintageous.svg?branch=master)](https://travis-ci.org/NeoVintageous/NeoVintageous) [![Build status](https://ci.appveyor.com/api/projects/status/g4pkv4ws1k2r1xna/branch/master?svg=true)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?label=stable)](https://github.com/NeoVintageous/NeoVintageous/tags) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Source Code](https://img.shields.io/badge/source-github-blue.svg)](https://github.com/NeoVintageous/NeoVintageous)

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

What follows are supplementary documentations about feature differences that are specific to Sublime Text. See the [Vim main help file](https://neovim.io/doc/user) for a complete guide on Vim.

Command | Description | Documentation | Dependencies | Notes
------- | ----------- | ------------- | ------------ | -----
[c | Jump backwards to the previous start of a change. | [diff](https://neovim.io/doc/user/diff.html#[c) | [Git Gutter](https://github.com/jisaacks/GitGutter) |
]c | Jump forwards to the next start of a change. | [diff](https://neovim.io/doc/user/diff.html#]c) | [Git Gutter](https://github.com/jisaacks/GitGutter) |
ctrl-w, H | Move the current window to be at the very top | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_H) | None | Only works in 2 col/row layouts
ctrl-w, J | Move the current window to be at the very bottom | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_J) | None | Only works in 2 col/row layouts
ctrl-w, K | Move the current view to be at the far left | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_K) | None | Only works in 2 col/row layouts
ctrl-w, L | Move the current window to be at the far right | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_L) | None | Only works in 2 col/row layouts
ctrl-w, s | Split current window in two | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_s) | [Origami](https://github.com/SublimeText/Origami)
ctrl-w, v | Split current window in two (vertically) | [windows.txt](https://neovim.io/doc/user/windows.html#CTRL-W_v) | [Origami](https://github.com/SublimeText/Origami)

### Plugins

#### Surround

A port of [tpope/vim-surround](https://github.com/tpope/vim-surround) is provided by default. *Not all unimpaired commands are implemented. Please open issues for missing features and commands.*

Documentation: [surround.txt](https://github.com/tpope/vim-surround/blob/master/doc/surround.txt).

#### Unimpaired

A port of [tpope/vim-unimpaired](https://github.com/tpope/vim-unimpaired) is provided by default. *Not all unimpaired commands are implemented. Please open issues for missing features and commands. Below is a table of what is currently available.*

Documentation: [unimpaired](https://raw.githubusercontent.com/tpope/vim-unimpaired/master/doc/unimpaired.txt).

Command | Description | Documentation | Dependencies | Notes
------- | ----------- | ------------- | ------------ | -----
[&lt;Space&gt; | Add [count] blank lines before the cursor. | [unimpaired](https://raw.githubusercontent.com/tpope/vim-unimpaired/master/doc/unimpaired.txt) | None |
]&lt;Space&gt; | Add [count] blank lines after the cursor. | [unimpaired](https://raw.githubusercontent.com/tpope/vim-unimpaired/master/doc/unimpaired.txt) | None |
[e | Exchange the current line with [count] lines above it. | [unimpaired](https://raw.githubusercontent.com/tpope/vim-unimpaired/master/doc/unimpaired.txt) | None |
]e | Exchange the current line with [count] lines below it. | [unimpaired](https://raw.githubusercontent.com/tpope/vim-unimpaired/master/doc/unimpaired.txt) | None |

### Command Palette

Command | Description
------- | -----------
NeoVintageous: Open My .vintageousrc File | Open the runtime configuration file for editing
NeoVintageous: Reload My .vintageousrc File | Reloads the runtime configuration file
NeoVintageous: Open Changelog | Opens the changelog in a view
NeoVintageous: Open Readme | Opens the readme in a view
Preferences: NeoVintageous Settings – Default | Opens the default settings
Preferences: NeoVintageous Settings – User | Opens the settings file for editing

### Toggle command

Use the official [ToggleNeoVintageous](https://github.com/NeoVintageous/ToggleNeoVintageous) plugin which provides a command to toggle NeoVintageous.

### The .vintageousrc file

A feature comparative to the [`.vimrc`](https://neovim.io/doc/user/usr_05.html#05.1) file.

The file is located at `Packages/User/.vintageousrc` and is read during startup.

There is limited support, the following are supported in basic use-cases: `:let mapleader=`, `:map`, `:unmap` `:nmap`, `:nunmap` `:omap`, `:ounmap` `:vmap`, and `:vunmap`.

The character " (the double quote mark) starts a comment.

Example

    :let mapleader=,

    " Enter command line mode using space
    :nmap <space> :

    " Visually select all content using ,a
    :nmap <leader>a ggvG

    " Scroll viewport faster ctrl+e and ctrl+y
    :nmap <C-e> 3<C-e>
    :nmap <C-y> 3<C-y>

    " Scroll up using space
    :nmap <space> <C-u>

    " Scroll down using shift-enter
    :nmap <S-cr> <C-d>

Read more about mappings in the [Vim main help file](https://neovim.io/doc/user/map.html).

### Modelines

A feature comparative to [Vim Modeline](https://neovim.io/doc/user/options.html#modeline).

Set options local to the view by declaring them in the source code file itself.

Example

    # sublime: gutter false
    # sublime: translate_tab_to_spaces true
    # sublime: rulers [80, 120]
    # sublime: tab_size 4

Read more about modeline in the [Vim main help file](https://neovim.io/doc/user/options.html#modeline).

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
