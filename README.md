![NeoVintageous Logo](res/neovintageous.png)

An advanced Vim emulation layer for Sublime Text.

[![Build Status](https://img.shields.io/travis/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://travis-ci.org/NeoVintageous/NeoVintageous) [![Build status](https://img.shields.io/appveyor/ci/gerardroche/neovintageous/master.svg?style=flat-square)](https://ci.appveyor.com/project/gerardroche/neovintageous/branch/master) [![Coverage Status](https://img.shields.io/coveralls/NeoVintageous/NeoVintageous/master.svg?style=flat-square)](https://coveralls.io/github/NeoVintageous/NeoVintageous?branch=master) [![Minimum Sublime Version](https://img.shields.io/badge/sublime-%3E%3D%203.0-brightgreen.svg?style=flat-square)](https://sublimetext.com) [![Latest Stable Version](https://img.shields.io/github/tag/NeoVintageous/NeoVintageous.svg?style=flat-square&label=stable)](https://github.com/NeoVintageous/NeoVintageous/tags) [![GitHub stars](https://img.shields.io/github/stars/NeoVintageous/NeoVintageous.svg?style=flat-square)](https://github.com/NeoVintageous/NeoVintageous/stargazers) [![Downloads](https://img.shields.io/packagecontrol/dt/NeoVintageous.svg?style=flat-square)](https://packagecontrol.io/packages/NeoVintageous)

Neovintageous is a project that seeks to continue the development of the discontinued Vintageous plugin.

* Open source
* Highly configurable
* Strong defaults
* Drop-in replacement for Vintageous
* Integrates with [GitGutter](https://github.com/jisaacks/GitGutter), [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter3) and [Origami](https://github.com/SublimeText/Origami)
* Plugins out-of-the-box: [Abolish](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/abolish.txt), [Commentary](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/commentary.txt), [Highlighted Yank](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt), [Surround](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/surround.txt), [Unimpaired](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/unimpaired.txt) and [Indent Object](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/indent-object.txt).

## Installation

### Package Control installation

Th# be preferred method of installation is [Package Control](https://packagecontrol.io/packages/NeoVintageous).


### Manual installation

Close Sublime Text, then download or clone this repository to a directory named **NeoVintageous** in the Sublime Text Packages directory for your platform:

OS | Command
-- | -----
Linux | `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/.config/sublime-text-3/Packages/NeoVintageous`
OSX | `git clone https://github.com/NeoVintageous/NeoVintageous.git ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/NeoVintageous`
Windows | `git clone https://github.com/NeoVintageous/NeoVintageous.git %APPDATA%\Sublime/ Text/ 3/Packages/NeoVintageous`

## Documentation

Neovintageous is an emulation of Vim (feature-parity is an ongoing effort). See the [`:help neovintageous`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) command to learn about the differences.

Vim's documentation system is accessible via the `:help` command, and is an extensive cross-referenced and hyperlinked reference. It's kept up-to-date with the software and can answer almost any question about Vim's functionality. An up-to-date version of Vim help, with hyperlinks, can be found on [appspot](https://vimhelp.appspot.com).

## Plugins

The following plugins are available out-of-the-box (feature-parity is an ongoing effort):

Plugin | Documentation | Original Vim Plugin
------ | ------------- | -------------------
Abolish | [`:help abolish`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/abolish.txt) | [vim-abolish](https://github.com/tpope/vim-abolish)
Commentary | [`:help commentary`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/commentary.txt) | [vim-commentary](https://github.com/tpope/vim-commentary)
Highlighted Yank | [`:help highlightedyank`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-highlightedyank](https://github.com/machakann/vim-highlightedyank)
Indent Object | [`:help indent-object`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/indent-object.txt) | [vim-indent-object](https://github.com/michaeljsmith/vim-indent-object)
Multiple Cursors | [`:help multiple-cursors`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt) | [vim-multiple-cursors](https://github.com/terryma/vim-multiple-cursors)
Surround | [`:help surround`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/surround.txt) | [vim-surround](https://github.com/tpope/vim-surround)
Unimpaired | [`:help unimpaired`](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/unimpaired.txt) | [vim-unimpaired](https://github.com/tpope/vim-unimpaired)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Credits

Neovintageous is a fork of the discontinued Vintageous plugin.

## License

Released under the [GPL-3.0-or-later License](LICENSE).
