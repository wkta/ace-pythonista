

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons. This should be used
    as a decorator -not a metaclass- to the class that should be a singleton.

    The decorated class can define one `__init__` function that takes only the `self`
    argument. Also, the decorated class cannot be inherited from.

    Other than that, there are no restrictions that apply to the decorated class.
    To get the singleton instance, use the `instance` method.
    Trying to use `__call__` will result in a `TypeError` being raised.
    """

    def __init__(self, decorated):
        self._decorated = decorated
        self._instance = None

    def instance(self):
        if self._instance is None:
            self._instance = self._decorated()
        return self._instance

    def __call__(self):
        err_msg = 'Singletons must be accessed through `instance()`'
        raise TypeError(err_msg)

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
