import numpy as np
from hash import KHash


class BloomFilter:
    def __init__(self, nums, k, n):
        self.khash = KHash(k)
        self.bits = [0 for _ in range(n)]
        self.n = n
        self.hash(nums)

    def hash(self, nums):
        for num in nums:
            random_bits = (self.khash.hash(num) % self.n).tolist()
            for bit in random_bits:
                self.bits[bit] = 1

    def insert(self, number):
        random_bits = (self.khash.hash(number) % self.n).tolist()
        for bit in random_bits:
            self.bits[bit] = 1

    def find(self, number):
        random_bits = (self.khash.hash(number) % self.n).tolist()
        for bit in random_bits:
            if self.bits[bit] == 0:
                return False
        return True

    def __del__(self):
        del self.khash
        del self.bits
        del self.n


obj = BloomFilter([25, 70, 56], 5, 50)
print(obj.find(26))
del obj
