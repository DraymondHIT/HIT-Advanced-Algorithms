import numpy as np

epsilon = 1e-10
INT_MAX = 100


class Graph:
    def __init__(self, n):
        self.n = n
        self.graph = np.zeros((n, n))
        for i in range(n):
            for j in range(i, self.n):
                if i == j:
                    self.graph[i][j] = INT_MAX
                else:
                    self.graph[i][j] = np.random.uniform(0+epsilon, 1)
                    self.graph[j][i] = self.graph[i][j]

    def prim(self):
        LOWCOST = np.zeros(self.n)
        CLOSEST = np.zeros(self.n, dtype=int)
        ans = np.zeros((self.n - 1, 3))

        k, weight = 0, 0
        for i in range(1, self.n):
            LOWCOST[i] = self.graph[0][i]
            CLOSEST[i] = 0

        for i in range(1, self.n):
            min = INT_MAX
            for j in range(1, self.n):
                if LOWCOST[j] < min:
                    min = LOWCOST[j]
                    k = j

            weight += min
            ans[i - 1][0] = CLOSEST[k]
            ans[i - 1][1] = k
            ans[i - 1][2] = self.graph[CLOSEST[k]][k]
            LOWCOST[k] = INT_MAX - 1
            for j in range(1, self.n):
                if self.graph[k][j] < LOWCOST[j] and abs(LOWCOST[j] - INT_MAX + 1) > 0.001:
                    LOWCOST[j] = self.graph[k][j]
                    CLOSEST[j] = k

        return weight, ans

