from hash import hash_func
import random
import numpy as np


class MinHash:
    def __init__(self):
        self.primeNUmber = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]

    def similarity(self, data, hash_funcs):
        MAX = 100000000
        M, N, R = len(data), len(data[0]), len(hash_funcs)

        HashTable = [[hash_func.random(i) for i in range(M)] for hash_func in hash_funcs]

        rt = [[MAX] * N for _ in range(R)]

        for r in range(R):
            for n in range(N):
                for m in range(M):
                    if data[m][n] == 0:
                        continue
                    rt[r][n] = min(rt[r][n], HashTable[r][m])
        return rt

    def run(self, data, keys, n_hash_funcs, c):
        hash_funcs = [hash_func(random.choice(self.primeNUmber), random.randint(1, 200), len(data)) for _ in range(n_hash_funcs)]
        minHashTable = np.array(self.similarity(data, hash_funcs))
        assert minHashTable.shape[1] == len(data[0])
        ans = []
        for i in range(len(keys)-1):
            for j in range(i+1, len(keys)):
                if np.sum(minHashTable[:, i] == minHashTable[:, j]) >= minHashTable.shape[0] * c:
                    ans.append((keys[i], keys[j]))
        # print(minHashTable)
        # print(ans)

        return ans
