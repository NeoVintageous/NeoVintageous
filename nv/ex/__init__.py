
command_names = []  # Used to provide completions on the ex command line.


def command(name, abbrev):
    # Register the name of an ex command with command_names.
    #
    # Meant to be imported like this:
    #
    #     from NeoVintageous.nv import ex
    #     ...
    #     @ex.command('foo', 'f')
    #     class ExFooCommand(...): ...

    command_names.append((name, abbrev))

    def inner(f):
        return f

    return inner
