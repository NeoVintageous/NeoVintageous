from NeoVintageous.nv.vi import inputs  # noqa: F401
from NeoVintageous.nv.vi.cmd_base import ViMotionDef  # noqa: F401
from NeoVintageous.nv.vi.cmd_base import ViOperatorDef  # noqa: F401
from NeoVintageous.nv.vim import INPUT_AFTER_MOTION  # noqa: F401
from NeoVintageous.nv.vim import INPUT_INMEDIATE  # noqa: F401
from NeoVintageous.nv.vim import INPUT_VIA_PANEL  # noqa: F401
from NeoVintageous.nv.vim import INTERNAL_NORMAL  # noqa: F401
from NeoVintageous.nv.vim import NORMAL  # noqa: F401
from NeoVintageous.nv.vim import OPERATOR_PENDING  # noqa: F401
from NeoVintageous.nv.vim import SELECT  # noqa: F401
from NeoVintageous.nv.vim import VISUAL  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_BLOCK  # noqa: F401
from NeoVintageous.nv.vim import VISUAL_LINE  # noqa: F401


mappings = {
    NORMAL: {},
    OPERATOR_PENDING: {},
    SELECT: {},
    VISUAL_BLOCK: {},
    VISUAL_LINE: {},
    VISUAL: {}
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
