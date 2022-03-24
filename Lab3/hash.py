import numpy as np
from numpy import random


class KHash:
    def __init__(self, k):
        self.k = k
        self.p = 241
        self.a = random.randint(low=1, high=self.p, size=self.k)
        self.b = random.randint(low=0, high=self.p, size=self.k)

    def hash(self, number):
        return (self.a * number + self.b) % self.p
