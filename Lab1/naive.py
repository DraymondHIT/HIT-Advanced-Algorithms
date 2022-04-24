class Naive:
    """
    使用naive方法实现集合的相似性连接
    """
    def __init__(self):
        pass

    @staticmethod
    def intersection(list1, list2):
        sum = 0
        for element1 in list1:
            for element2 in list2:
                if element1 == element2:
                    sum += 1
        return sum

    def run(self, corpus, c: float):
        ans = set()
        for i in range(len(corpus)-1):
            for j in range(i+1, len(corpus)):
                inter = self.intersection(corpus[i], corpus[j])  # 交集大小
                union = len(corpus[i]) + len(corpus[j]) - inter  # 并集大小
                if inter >= c * union:
                    ans.add((i, j))
        return ans
