from functools import wraps


class Int4(int):
    def __new__(cls, i):
        return super(Int4, cls).__new__(cls, i & 0xf)


def add_special_method(cls, name):
    mname = '__{}__'.format(name)

    @wraps(getattr(cls, mname))
    def convert_to_cls(self, other):
        bound_original = getattr(super(cls, self), mname)
        return type(self)(bound_original(other))

    setattr(cls, mname, convert_to_cls)

    for m in ('add', 'sub', 'mul', 'floordiv', 'mod', 'pow',
              'lshift', 'rshift', 'and', 'xor', 'or'):
        add_special_method(Int4, m)
        add_special_method(Int4, 'r' + m)  # reverse operation

