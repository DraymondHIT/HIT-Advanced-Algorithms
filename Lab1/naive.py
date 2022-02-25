class Naive:
    """
    使用naive方法实现集合的相似性连接
    """
    def __init__(self):
        pass

    @staticmethod
    def intersection(list1: list, list2: list) -> int:
        i = j = 0
        len1 = len(list1)
        len2 = len(list2)
        sum = 0
        while i < len1 and j < len2:
            if list1[i] == list2[j]:
               sum += 1
               i += 1
               j += 1
            elif list1[i] < list2[j]:
                i += 1
            else:
                j += 1
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
