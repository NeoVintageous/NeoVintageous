from NeoVintageous.lib.vi.utils import modes
from NeoVintageous.lib.vi.cmd_base import ViOperatorDef  # FIXME # noqa: F401
from NeoVintageous.lib.vi.cmd_base import ViMotionDef  # FIXME # noqa: F401
from NeoVintageous.lib.vi import inputs  # FIXME # noqa: F401


NORMAL_MODE = modes.NORMAL
VISUAL_MODE = modes.VISUAL
VISUAL_BLOCK_MODE = modes.VISUAL_BLOCK
OPERATOR_PENDING_MODE = modes.OPERATOR_PENDING
INTERNAL_NORMAL_MODE = modes.INTERNAL_NORMAL

mappings = {
    modes.NORMAL: {},
    modes.OPERATOR_PENDING: {},
    modes.VISUAL: {},
    modes.VISUAL_LINE: {},
    modes.VISUAL_BLOCK: {},
    modes.SELECT: {},
}

classes = {}


def register(seq, modes, *args, **kwargs):
    """
    Register a 'key sequence' to 'command' mapping with NeoVintageous.

    The registered key sequence must be known to NeoVintageous. The
    registered command must be a ViMotionDef or ViOperatorDef.

    The decorated class is instantiated with `*args` and `**kwargs`.

    @keys
      A list of (`mode`, `sequence`) pairs to map the decorated
      class to.
    """
    def inner(cls):
        for mode in modes:
                mappings[mode][seq] = cls(*args, **kwargs)
                classes[cls.__name__] = cls
        return cls
    return inner
