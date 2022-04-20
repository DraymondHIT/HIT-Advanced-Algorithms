import random
import numpy as np
import hashlib
import time


class MinHash:
    def __init__(self, b, r):
        self.b = b
        self.r = r

    # @staticmethod
    # def singleHash(matrix):
    #     """
    #     生成单一的Hash函数
    #     """
    #     seqSet = [i for i in range(matrix.shape[0])]
    #     result = [-1 for _ in range(matrix.shape[1])]
    #     count = 0
    #     while len(seqSet) > 0:
    #         randomSeq = random.choice(seqSet)
    #         for i in range(matrix.shape[1]):
    #             if matrix[randomSeq][i] != 0:
    #                 if result[i] == -1:
    #                     result[i] = randomSeq
    #                     count += 1
    #                 elif randomSeq < result[i]:
    #                     result[i] = randomSeq
    #         if count == matrix.shape[1]:
    #             break
    #         seqSet.remove(randomSeq)
    #     return result

    def singleHash(self, data, n):
        seq = [i for i in range(n)]
        result = [n for _ in range(len(data))]
        seq = np.random.permutation(seq)
        for i in range(len(result)):
            minhash = n
            for element in data[i]:
                if seq[element] < minhash:
                    result[i] = element
                    minhash = seq[element]
        return result


    def sigMatrix(self, data, n_elements, n_hash_funcs):
        """
        计算sigMatrix
        """
        result = []
        for i in range(n_hash_funcs):
            single = self.singleHash(data, n_elements)
            result.append(single)
        return np.array(result)

    def minHash(self, data, n_elements):
        """
        LSH算法
        """
        hashBuckets = {}
        n = self.b * self.r

        # time_start = time.time()
        sigMatrix = self.sigMatrix(data, n_elements, n)
        # print(sigMatrix)
        # time_end = time.time()
        # print(time_end - time_start)

        begin, end = 0, self.r
        count = 0

        while end <= sigMatrix.shape[0]:
            count += 1
            for colNum in range(sigMatrix.shape[1]):
                # generate the hash object
                hashObj = hashlib.md5()

                # calculate the hash value
                band = str(sigMatrix[begin: begin + self.r, colNum]) + str(count)
                hashObj.update(band.encode())
                tag = hashObj.hexdigest()

                # update the dictionary
                if tag not in hashBuckets:
                    hashBuckets[tag] = [colNum]
                elif colNum not in hashBuckets[tag]:
                    hashBuckets[tag].append(colNum)
            begin += self.r
            end += self.r

        return hashBuckets

    def run(self, data, n):
        # time_start = time.time()
        hashBucket = self.minHash(data, n)
        # time_end = time.time()
        # print(time_end-time_start)

        query = [_ for _ in range(len(data))]
        result = set()

        # time_start = time.time()
        for key in hashBucket:
            result = result.union(set([(min(col1, col2), max(col1, col2)) for col1 in hashBucket[key] for col2 in hashBucket[key]]))
        # time_end = time.time()
        # print(time_end - time_start)

        return len(result) - len(query)
