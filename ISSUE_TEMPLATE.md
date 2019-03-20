<!--

Do you want to ask a question? Are you looking for support? The Sublime Text message board is the best place for getting support: https://forum.sublimetext.com.

-->

### Description

### Steps to Reproduce

### Expected behaviour

### Actual behaviour

### Versions

Show the Sublime Text console log: `Menu > View > Show Console`.

Example: `startup, version: 3200 linux x64 channel: stable`

### Additional Information

Any additional information, configuration, or data that might be necessary to reproduce the issue.

Show the Sublime Text console log: `Menu > View > Show Console`.

Command and input logging are enabled by running the following commands in input box at the bottom of the console: `sublime.log_commands(True)` and `sublime.log_input(True)`.

Running `$ SUBLIME_NEOVINTAGEOUS_DEBUG=y; subl` (unix), `> set SUBLIME_NEOVINTAGEOUS_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"` (windows), will run NeoVintageous in debug mode. Debug messages are printed to the console log. See the [contributing guide](https://github.com/NeoVintageous/NeoVintageous/blob/master/CONTRIBUTING.md) for additional debugging instructions.

You may also want to review the help file: `:help neovintageous`, or visit the [online help file](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt).
