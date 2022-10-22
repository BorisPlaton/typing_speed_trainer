class CallableString(str):

    def __call__(self, *args):
        return f"'{self.base_key}:{':'.join(map(str, args))}'" if args else self.base_key

    def __init__(self, base_key: str):
        self.base_key = base_key


class KeyField:

    def __get__(self, instance, owner):
        return self.base_key

    def __init__(self, base_key: str):
        self.base_key = CallableString(base_key)
