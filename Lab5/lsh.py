import numpy as np
import random
import time
import distance


class LSHBuilder:
    methods = ["uniform",
               "weighted_uniform",
               "approx_degree",
               "exact_degree"]

    @staticmethod
    def build(d, r, k, L, w, validate=False):
        return E2LSH(k, L, w, d, r, validate)

    @staticmethod
    def invoke(lsh, method, queries, runs):
        assert method in LSHBuilder.methods
        if method == "uniform":
            res = lsh.uniform_query(queries, runs)
        elif method == "weighted_uniform":
            res = lsh.weighted_uniform_query(queries, runs)
        elif method == "approx_degree":
            res = lsh.approx_degree_query(queries, runs)
        else:
            res = lsh.exact_degree_query(queries, runs)

        return res


class LSH:

    def preprocess(self, X):
        self.X = X
        n = len(X)
        hvs = self._hash(X)
        self.tables = [{} for _ in range(self.L)]
        for i in range(n):
            for j in range(self.L):
                h = self._get_hash_value(hvs[i], j)
                self.tables[j].setdefault(h, set()).add(i)

    def preprocess_query(self, Y):
        """Collect buckets, bucket sizes, and prefix_sums
        to quickly answer queries."""
        query_buckets = [[] for _ in range(len(Y))]
        query_size = [0 for _ in range(len(Y))]
        bucket_sizes = [0 for _ in range(len(Y))]
        prefix_sums = [[0 for _ in range(self.L)] for _ in range(len(Y))]
        query_results = [set() for _ in range(len(Y))]

        hvs = self._hash(Y)
        for j, q in enumerate(hvs):
            buckets = [(i, self._get_hash_value(q, i)) for i in range(self.L)]
            query_buckets[j] = buckets
            s = 0
            elements = set()
            for i, (table, bucket) in enumerate(buckets):
                s += len(self.tables[table].get(bucket, []))
                elements |= self.tables[table].get(bucket, set())
                prefix_sums[j][i] = s
            elements = set(x for x in elements
                           if self.is_candidate_valid(Y[j], self.X[x]))
            bucket_sizes[j] = s
            query_size[j] = len(elements)
            query_results[j] = elements

        return (query_buckets, query_size, query_results,
                bucket_sizes, prefix_sums)

    def get_query_size(self, Y):
        _, query_size, _, _, _ = self.preprocess_query(Y)
        return query_size

    def uniform_query(self, Y, runs=100):
        query_bucket, sizes, query_results, _, _ = self.preprocess_query(Y)
        results = {i: [] for i in range(len(Y))}
        for j in range(len(Y)):
            for _ in range(sizes[j] * runs):
                if len(query_results[j]) == 0:
                    results[j].append(-1)
                    continue
                while True:
                    table, bucket = query_bucket[j][random.randrange(0, self.L)]
                    elements = list(self.tables[table].get(bucket, [-1]))
                    p = random.choice(elements)
                    if p != -1 and self.is_candidate_valid(Y[j], self.X[p]):
                        results[j].append(p)
                        break
        return results

    def weighted_uniform_query(self, Y, runs=100):
        from bisect import bisect_right
        query_buckets, query_size, elements, bucket_sizes, prefix_sums = self.preprocess_query(Y)
        results = {i: [] for i in range(len(Y))}

        for j in range(len(Y)):
            for _ in range(query_size[j] * runs):
                if len(elements[j]) == 0:
                    results[j].append(-1)
                    continue
                while True:
                    i = random.randrange(bucket_sizes[j])
                    pos = bisect_right(prefix_sums[j], i)
                    table, bucket = query_buckets[j][pos]
                    p = random.choice(list(self.tables[table][bucket]))
                    if self.is_candidate_valid(Y[j], self.X[p]):
                        results[j].append(p)
                        break
        return results

    def approx_degree_query(self, Y, runs=100):
        from bisect import bisect_right
        query_buckets, query_size, _, bucket_sizes, prefix_sums = self.preprocess_query(Y)
        results = {i: [] for i in range(len(Y))}

        for j in range(len(Y)):

            for _ in range(query_size[j] * runs):
                if bucket_sizes[j] == 0:
                    results[j].append(-1)
                    continue
                while True:
                    i = random.randrange(bucket_sizes[j])
                    pos = bisect_right(prefix_sums[j], i)
                    table, bucket = query_buckets[j][pos]
                    p = random.choice(list(self.tables[table][bucket]))
                    # discard not within distance threshold
                    if not self.is_candidate_valid(Y[j], self.X[p]):
                        continue
                    D = self.approx_degree(query_buckets[j], p)
                    if random.randint(1, D) == D:  # output with probability 1/D
                        results[j].append(p)
                        break
        return results

    def exact_degree_query(self, Y, runs=100):
        from bisect import bisect_right
        query_buckets, query_size, _, bucket_sizes, prefix_sums = self.preprocess_query(Y)
        results = {i: [] for i in range(len(Y))}

        for j in range(len(Y)):

            for _ in range(query_size[j] * runs):
                if bucket_sizes[j] == 0:
                    results[j].append(-1)
                    continue
                while True:
                    i = random.randrange(bucket_sizes[j])
                    pos = bisect_right(prefix_sums[j], i)
                    table, bucket = query_buckets[j][pos]
                    p = random.choice(list(self.tables[table][bucket]))
                    # discard not within distance threshold
                    if not self.is_candidate_valid(Y[j], self.X[p]):
                        continue
                    D = self.exact_degree(query_buckets[j], p)
                    if random.randint(1, D) == D:  # output with probability 1/D
                        results[j].append(p)
                        break
        return results

    def approx_degree(self, buckets, q):
        num = 0
        L = len(buckets)
        while num < L:
            num += 1
            table, bucket = buckets[random.randrange(0, L)]
            if q in self.tables[table].get(bucket, set()):
                break
        return L // num

    def exact_degree(self, buckets, q):
        cnt = 0
        for table, bucket in buckets:
            if q in self.tables[table].get(bucket, set()):
                cnt += 1
        return cnt

    def is_candidate_valid(self, q, x):
        pass


class E2LSH(LSH):
    def __init__(self, k, L, w, d, r, validate=True, seed=3):
        np.random.seed(seed)
        random.seed(seed)
        self.A = np.random.normal(0.0, 1.0, (d, k * L))
        self.b = np.random.uniform(0.0, w, (1, k * L))
        self.w = w
        self.L = L
        self.k = k
        self.r = r
        self.validate = validate

    def _hash(self, X):
        # X = np.transpose(X)
        hvs = np.matmul(X, self.A)
        hvs += self.b
        hvs /= self.w
        return np.floor(hvs).astype(np.int32)

    def _get_hash_value(self, arr, idx):
        return tuple(arr[idx * self.k: (idx + 1) * self.k])

    def is_candidate_valid(self, q, x):
        # print(distance.l2(q, x))
        return not self.validate or distance.l2(q, x) <= self.r

    def __str__(self):
        return f"E2LSH(k={self.k}, L={self.L}, w={self.w})"

    def __repr__(self):
        return f"k_{self.k}_L_{self.L}_w_{self.w}"


def test_euclidean():
    d = 10
    n = 10000
    m = 10
    w = 4.0
    k = 2
    L = 3
    r = 4
    lsh = E2LSH(k, L, w, d, r)
    X = np.random.normal(0.0, 1.0, (n, d))
    lsh.preprocess(X)
    Y = np.random.normal(0.0, 1.0, (m, d))
    s = time.time()
    lsh.weighted_uniform_query(Y)
    print(time.time() - s)


if __name__ == "__main__":
    test_euclidean()
