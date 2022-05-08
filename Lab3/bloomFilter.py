from hash import KHash
from datatype import Int4


class BloomFilter:
    def __init__(self, objects, k, n):
        self.khash = KHash(k, n)
        self.pinCnt = [Int4(0) for _ in range(n)]
        self.hash(objects)

    def hash(self, objects):
        for obj in objects:
            random_bits = self.khash.hash(hash(obj)).tolist()
            for bit in random_bits:
                self.pinCnt[bit] += 1

    def insert(self, obj):
        random_bits = self.khash.hash(hash(obj)).tolist()
        for bit in random_bits:
            self.pinCnt[bit] += 1

    def find(self, obj):
        random_bits = self.khash.hash(hash(obj)).tolist()
        for bit in random_bits:
            if self.pinCnt[bit] == 0:
                return False
        return True

    def delete(self, obj):
        assert self.find(obj)
        random_bits = self.khash.hash(hash(obj)).tolist()
        for bit in random_bits:
            self.pinCnt[bit] -= 1

    def __del__(self):
        del self.khash
        del self.pinCnt

