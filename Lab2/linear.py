class Linear:
    def __init__(self, corpus, k):
        self.corpus = corpus
        self.k = k

    @staticmethod
    def swap(a, i, j):
        if i == j:
            return
        temp = a[j]
        a[j] = a[i]
        a[i] = temp

    def findMid(self, a, l, r):
        if l == r:
            return l
        i = l
        n = 0
        for i in range(l, r-4, 5):
            a[i: i + 5] = sorted(a[i: i + 5])
            n = i - l
            self.swap(a, l + n // 5, i + 2)
        ## 处理剩余元素
        if r - 4 > l:
            i += 5
            n = i - l
        num = r - i
        if num > 0:
            a[i:i+num] = sorted(a[i:i+num])
            n = i - l
            self.swap(a, l + n // 5, i + num // 2)
        n //= 5
        if n == l:
            return l
        return self.findMid(a, l, l + n)

    def partition(self, a, l, r, p):
        self.swap(a, p, l)
        i = l
        j = r - 1
        pivot = a[l]
        while i < j:
            while a[j] >= pivot and i < j:
                j -= 1
            a[i] = a[j]
            while a[i] <= pivot and i < j:
                i += 1
            a[j] = a[i]
        a[i] = pivot
        return i

    def select(self, a, l, r, k):
        p = self.findMid(a, l, r)
        i = self.partition(a, l, r, p)
        m = i - l + 1
        if m == k:
            return a[i]
        elif m > k:
            return self.select(a, l, i, k)
        else:
            return self.select(a, i + 1, r, k - m)

    def run(self):
        result = {}
        temp = self.corpus["uniform"]
        result["uniform"] = self.select(temp, 0, len(temp), self.k)
        temp = self.corpus["normal"]
        result["normal"] = self.select(temp, 0, len(temp), self.k)
        temp = self.corpus["zipf"]
        result["zipf"] = self.select(temp, 0, len(temp), self.k)
        return result

        # 测试样例
        # a = [3, 0, 7, 6, 5, 9, 8, 2, 1, 74, 13, 11, 17, 16, 75, 19, 18, 12, 40, 14, 23, 21,
        #      27, 26, 25, 69, 28, 22, 20, 24, 53, 31, 37, 36, 35, 39, 38, 32, 50, 54, 43, 41, 47, 46, 45, 49,
        #      48, 42, 10, 44, 33, 51, 57, 56, 55, 59, 58, 52, 30, 34, 63, 61, 67, 66, 65, 29, 68, 62, 60, 64,
        #      73, 71, 77, 76, 15, 79, 78, 72, 70, 4]
        # result = self.select(a, 0, 80, 13)
        # print(result)


# 测试用, Linear()中参数为任意值
# linear = Linear(1, 2)
# linear.run()
