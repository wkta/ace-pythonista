"""
useful for creating modules that can be easily hacked/extended,
via the dependency injection pattern.

e.g. imagine targ_pm the target,
 an example of PowerModule that uses a "particles" sub-module.
 
Therefore thanks to the current file,
I'll be able to do this:

targ_pm.injector.register('particles', '..othermodpath.betterpartices')

that is replace the standard submodule by smth else, maybe better.
It's the same method for adding things that even don't exist.

"""
import importlib


class _Injector:
    def __init__(self, defaultpackage):
        self._mcache = dict()
        self.codesources = dict()
        self._p = defaultpackage
        
    def register(self, mname, mpath):
        self.codesources[mname] = mpath
        if mname in self._mcache:
            del self._mcache[mname]

    def fetch(self, v):  # used only by PowerCode, a priori
        if v not in self._mcache:
            try:
                print('injector lazy import ->', v)
                mpath = self.codesources[v]
                self._mcache[v] = importlib.import_module(mpath, package=None)
            except KeyError:
                self._mcache[v] = importlib.import_module(v, package=self._p)
        
        return self._mcache[v]

    def __getitem__(self, v):
        return self._fetch(v)


class PowerModule:
    # injector + lazy loading are built-in
    
    def __init__(self, packag):
        self.injector = _Injector(packag)

    def can_get(self, attr_name):
        try:
            t = self.injector.fetch(attr_name)
            return True
        except ModuleNotFoundError:
            return False

    def __getattr__(self, aname):
        x = self.__class__.__name__
        print(f'{x}:getattr looks for "{aname}"')
        return self.injector.fetch(aname)
