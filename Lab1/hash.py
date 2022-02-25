class hash_func:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def random(self, x):
        return (self.a * x + self.b) % self.c
