# CONTRIBUTING

## Documentation

To open the help file run `:help neovintageous`, or [view it online](https://github.com/NeoVintageous/NeoVintageous/blob/master/res/doc/neovintageous.txt).

## Testing

The [UnitTesting](https://github.com/randy3k/UnitTesting) package is used to run the tests. Install it, open the Command Palette, type "UnitTesting", press `Enter`, and input **"NeoVintageous"** as the package to test.

## Debugging

### Console

View the console: **Menu > View > Show Console**

### Performance

View plugin performance profile: **Menu > Tools > Developer > Profile Plugins**

### Logging

Enable command and input logging (run in the input at the bottom of the console):

```
sublime.log_commands(True)
sublime.log_input(True)
```

Enable debug logging by setting the environment variable `SUBLIME_NEOVINTAGEOUS_DEBUG`:

Linux

```
$ export SUBLIME_NEOVINTAGEOUS_DEBUG=y; subl
```

Windows

```
> set SUBLIME_NEOVINTAGEOUS_DEBUG=y& "C:\Program Files\Sublime Text 3\subl.exe"
```

## Reverting to a freshly installed state

* [Reverting to a freshly installed state](https://www.sublimetext.com/docs/3/revert.html) (Sublime Text Documentation)
* [Reverting Sublime Text to its default configuration](http://docs.sublimetext.info/en/latest/extensibility/packages.html?highlight=fresh#reverting-sublime-text-to-its-default-configuration) (Unofficial Sublime Text Documentation)

### Reverting vs Cleaning

On Linux and OSX, [this script](https://github.com/gerardroche/dotfiles/blob/master/src/bin/sublime-clean) can be used to clean caches, indexes, workspaces, sessions, etc. Note that cleaning and reverting are not the same: **reverting** removes installed packages and configurations, **cleaning** only removes files that are generated at runtime e.g. caches, indexes, sessions.
