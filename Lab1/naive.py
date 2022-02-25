class Naive:
    """
    使用naive方法实现集合的相似性连接
    """
    def __init__(self):
        pass

    @staticmethod
    def intersection(list1: list, list2: list) -> int:
        sum = 0
        for element1 in list1:
            for element2 in list2:
                if element1 == element2:
                    sum += 1
        return sum

    def run(self, corpus: dict, c: float):
        keys = sorted(list(corpus.keys()))
        ans = set()
        for i in range(len(keys)-1):
            for j in range(i+1, len(keys)):
                inter = self.intersection(corpus[keys[i]], corpus[keys[j]])  # 交集大小
                union = len(corpus[keys[i]]) + len(corpus[keys[j]]) - inter  # 并集大小
                if inter >= c * union:
                    ans.add((i, j))
        return ans
