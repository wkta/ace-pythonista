import re


def camel_case_format(str_with_underscore):
    words = [word.capitalize() for word in str_with_underscore.split('_')]
    return "".join(words)


def underscore_format(gname):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', gname)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


EnumSeed = lambda gt,c0: {i: ename for (i, ename) in zip(gt, range(c0,c0+len(gt)))}


class _CustomIter:
    """
    to make PseudoEnum instances -iterable-
    """
    def __init__(self, ref_penum):
        self._ref = ref_penum
        self._curr_idx = 0

    def __iter__(self):
        return self
 
    def __next__(self):
        if self._curr_idx >= self._ref.size:
            raise StopIteration
        else:
            idx = self._ref.order[self._curr_idx]
            self._curr_idx += 1
            return self._ref.content[idx]


class PseudoEnum:
    def __init__(self, given_str_iterable, enumcode0=0):
        self._order = tuple(given_str_iterable)
        self._size = len(self._order)

        self._first = enumcode0
        self.content = EnumSeed(given_str_iterable, enumcode0)

        tmp_omega = list()
        tmp_names_pep8f = list()
        for k in self._order:
            tmp_omega.append(self.content[k])
            tmp_names_pep8f.append(underscore_format(k))
        self.omega = tuple(tmp_omega)
        self._names_pep8f = tuple(tmp_names_pep8f)

    def __getattr__(self, name):
        if name in self.content:
            return self.content[name]
        raise AttributeError("object has no attribute '{}'".format(name))

    @property
    def underscored_names(self):
        return self._names_pep8f

    @property
    def first(self):
        return self._first

    @property
    def order(self):
        return self._order

    @property
    def size(self):
        return self._size

    def __iter__(self):
        return _CustomIter(self)
