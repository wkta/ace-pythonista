from PowerModule import PowerModule as _Pm
import os as _os


REG_CONSTANT = 'hello world!'


class _ModuleIface:
    event = None
    color = None
    xyz = None


pygame =_ModuleIface()


class _My_Engine(_Pm):
    def __init__(self):
        global pygame
        print(_os.path.dirname(__file__))
        super().__init__(_os.path.dirname(__file__))
        del pygame
        self.injector.register('pygame', 'pygame')
        self.injector.register('plugin', 'implem_plugin.jojo')


_mobj_proxy = _My_Engine()


def __getattr__(v):
    if not _mobj_proxy.can_get(v):
        temp = _os.path.basename(__file__)
        nn = _os.path.splitext(temp)[0]
        raise AttributeError(f"module '{nn}' has no attribute '{v}'")
    else:
        return _My_Engine.__getattr__(_mobj_proxy, v)
