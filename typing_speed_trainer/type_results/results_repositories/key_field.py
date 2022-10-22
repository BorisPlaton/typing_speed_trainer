class KeyField(str):
    """
    It is a derivative of str class. Implements a `__call__` method.
    """

    def __call__(self, *args):
        """
        If arguments are passed, constructs a string with colons. Otherwise,
        returns itself.
        """
        return f"{self}:{':'.join(map(str, args))}" if args else self
