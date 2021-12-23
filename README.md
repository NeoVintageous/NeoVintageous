![NeoVintageous Logo](res/neovintageous.png)

An advanced Vim emulation layer for Sublime Text.

[![Continuous Integration](https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/NeoVintageous/NeoVintageous/actions/workflows/ci.yml) [![AppVeyor Build status](https://img.shields.io/appveyor/ci/gerardroche/neovintageous/master.svg?style=flat-square&label=appveyor)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Coveralls Coverage Status](https://img.shields.io/coveralls/NeoVintageous/NeoVintageous/master.svg?style=flat-square&label=coveralls)](https://coveralls.io/github/NeoVintageous/NeoVintageous?branch=master) [![Codecov Coverage Status](https://img.shields.io/codecov/c/github/NeoVintageous/NeoVintageous/master?style=flat-square&label=codecov)](https://codecov.io/gh/NeoVintageous/NeoVintageous/branch/master)

[![Latest Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?style=flat-square&label=version)](https://github.com/NeoVintageous/NeoVintageous/tags) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Downloads](https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square)](https://packagecontrol.io/packages/NeoVintageous)

NeoVintageous is a project that seeks to continue the development of the discontinued Vintageous plugin.

* Open source
* Highly configurable
* Strong defaults
* Drop-in replacement for Vintageous
* Integrates with [GitGutter](https://github.com/jisaacks/GitGutter), [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) and [Origami](https://github.com/SublimeText/Origami)
* Plugins out-of-the-box: [Abolish](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt), [Commentary](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt), [Highlighted Yank](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt), [Surround](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt), [Unimpaired](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) and [Indent Object](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt).

## Installation

### Package Control installation

The preferred method of installation is [Package Control](https://packagecontrol.io/packages/NeoVintageous).

To keep up to date with the latest beta releases add "NeoVintageous" to your Package Control settings, see [Package Control settings documentation](https://packagecontrol.io/docs/settings) for more information, for example:

```json
"install_prereleases": ["NeoVintageous"]
```

### Manual installation

Close Sublime Text, then download or clone this repository to a directory named **NeoVintageous** in the Sublime Text Packages directory for your platform:

OS | Command
-- | -----
Linux | `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`
OSX | `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`
Windows | `git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`

## Documentation

**NeoVintageous** is an emulation of Vim, feature-parity is an ongoing effort, some features are not implemented or implemented fully, and differences are not fully documented. See [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) to learn about some of the differences.

Vim's full documentation system is accessible via the `:help {subject}` command, and is an extensive cross-referenced and hyperlinked reference. It's kept up-to-date with the software and can answer almost any question about Vim's functionality. An up-to-date version of Vim help, with hyperlinks, can be found on [appspot](https://vimhelp.appspot.com).

## Plugins

A number of popular vim plugins have been ported and are available out-of-the-box.

Vim plugin feature-parity is an ongoing effort, some features are not implemented or implemented fully, and differences may not be fully documented. Please open issues to request missing features.

Plugin | Documentation | Original Vim Plugin
------ | ------------- | -------------------
Abolish | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-abolish](https://github.com/tpope/vim-abolish)
Commentary | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-commentary](https://github.com/tpope/vim-commentary)
Highlighted Yank | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-highlightedyank](https://github.com/machakann/vim-highlightedyank)
Indent Object | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
Multiple Cursors | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-multiple-cursors](https://github.com/terryma/vim-multiple-cursors)
Surround | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-surround](https://github.com/tpope/vim-surround)
Sneak | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-sneak](https://github.com/justinmk/vim-sneak)
Unimpaired | [`:help nv`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-unimpaired](https://github.com/tpope/vim-unimpaired)

## Contributing

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

NeoVintageous is a fork of the discontinued Vintageous plugin.

## License

Released under the [GPL-3.0-or-later License](LICENSE).
