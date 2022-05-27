import numpy as np
import random
import distance


class LSH:

    def __init__(self, k, L, w, d, r, seed=3):
        np.random.seed(seed)
        random.seed(seed)
        self.A = np.random.normal(0.0, 1.0, (d, k * L))
        self.b = np.random.uniform(0.0, w, (1, k * L))
        self.w = w
        self.L = L
        self.k = k
        self.r = r
        self.X = None
        self.Y = None

        self.tables = [{} for _ in range(self.L)]
        self.query_buckets = None
        self.query_size = None
        self.bucket_sizes = None
        self.prefix_sums = None
        self.query_results = None

        self.methods = ["uniform",
                        "weighted_uniform",
                        "approx_degree",
                        "exact_degree"]

    def get_methods(self):
        return self.methods

    def invoke(self, method, queries, runs, cached=False):
        assert method in self.methods
        if method == "uniform":
            res = self.uniform_query(queries, option="uniform", runs=runs, cached=cached)
        elif method == "weighted_uniform":
            res = self.uniform_query(queries, option="weighted", runs=runs, cached=cached)
        elif method == "approx_degree":
            res = self.degree_query(queries, option="approx_degree", runs=runs, cached=cached)
        else:
            res = self.degree_query(queries, option="exact_degree", runs=runs, cached=cached)

        return res

    def preprocess(self, X):
        self.X = X
        n = len(X)
        hvs = self._hash(X)
        for i in range(n):
            for j in range(self.L):
                h = self._get_hash_value(hvs[i], j)
                self.tables[j].setdefault(h, set()).add(i)

    def preprocess_query(self, Y, cached=False):
        if cached and (Y == self.Y).all():
            return

        self.Y = Y
        self.query_buckets = [[] for _ in range(len(Y))]
        self.query_size = np.zeros(len(Y)).astype(np.int32)
        self.bucket_sizes = np.zeros(len(Y)).astype(np.int32)
        self.prefix_sums = np.zeros((len(Y), self.L)).astype(np.int32)
        self.query_results = [set() for _ in range(len(Y))]

        hvs = self._hash(Y)
        for j, q in enumerate(hvs):
            buckets = [(i, self._get_hash_value(q, i)) for i in range(self.L)]
            self.query_buckets[j] = buckets
            s = 0
            query_elements = set()
            for i, (table, bucket) in enumerate(buckets):
                query_element = self.tables[table].get(bucket, set())
                s += len(query_element)
                query_elements |= query_element
                self.prefix_sums[j][i] = s
            query_elements = set(x for x in query_elements if self.is_candidate_valid(Y[j], self.X[x]))
            self.bucket_sizes[j] = s
            self.query_size[j] = len(query_elements)
            self.query_results[j] = query_elements

    def get_query_size(self, Y):
        self.preprocess_query(Y)
        return self.query_size

    def uniform_query(self, Y, option="uniform", runs=100, cached=False):
        assert option in ["uniform", "weighted"]
        self.preprocess_query(Y, cached)
        results = {i: [] for i in range(len(Y))}
        for j in range(len(Y)):
            if len(self.query_results[j]) == 0:
                results[j].append(-1)
                continue
            for _ in range(self.query_size[j] * runs):
                while True:
                    if option == "uniform":
                        table, bucket = self.query_buckets[j][random.randrange(0, self.L)]
                        elements = list(self.tables[table].get(bucket, [-1]))
                        p = random.choice(elements)
                    else:
                        p = self.random_choice(j)
                    if p != -1 and self.is_candidate_valid(Y[j], self.X[p]):
                        results[j].append(p)
                        break
        return results

    def degree_query(self, Y, option="approx_degree", runs=100, cached=False):
        assert option in ["approx_degree", "exact_degree"]
        self.preprocess_query(Y, cached)
        results = {i: [] for i in range(len(Y))}

        for j in range(len(Y)):
            for _ in range(self.query_size[j] * runs):
                if self.bucket_sizes[j] == 0:
                    results[j].append(-1)
                    continue
                while True:
                    p = self.random_choice(j)

                    if not self.is_candidate_valid(Y[j], self.X[p]):
                        continue
                    if option == "approx_degree":
                        D = self.approx_degree(self.query_buckets[j], p)
                    else:
                        D = self.exact_degree(self.query_buckets[j], p)
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

    def random_choice(self, j):
        assert self.Y is not None
        from bisect import bisect_right
        i = random.randrange(self.bucket_sizes[j])
        pos = bisect_right(self.prefix_sums[j], i)
        table, bucket = self.query_buckets[j][pos]
        p = random.choice(list(self.tables[table][bucket]))
        return p

    def _hash(self, X):
        hvs = np.matmul(X, self.A)
        hvs += self.b
        hvs /= self.w
        return np.floor(hvs).astype(np.int32)

    def _get_hash_value(self, arr, idx):
        return tuple(arr[idx * self.k: (idx + 1) * self.k])

    def is_candidate_valid(self, q, x):
        return distance.l2(q, x) <= self.r

    def __str__(self):
        return f"LSH(k={self.k}, L={self.L}, w={self.w})"

    def __repr__(self):
        return f"k_{self.k}_L_{self.L}_w_{self.w}"

