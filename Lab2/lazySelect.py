from sort import MergeSort
import numpy as np
import math


class LazySelect:
    def __init__(self, corpus, k):
        self.corpus = corpus
        self.k = k

    @staticmethod
    def randomSelect(data):
        return np.random.choice(data, int(pow(len(data), 0.75)), replace=True).tolist()

    @staticmethod
    def rank(list, element):
        assert element in list
        count = 0
        for _ in list:
            if _ < element:
                count += 1
        return count + 1

    def run(self, name_list):
        result = {}
        for name in name_list:
            temp = self.corpus[name][:]
            n = len(temp)
            epoch = 0

            while True:
                epoch += 1

                ## 从原数据集中抽取n^0.75个元素
                samples = self.randomSelect(temp)

                ## O(n)排序
                merge = MergeSort()
                samples = merge.run(samples)

                x = int(self.k * pow(n, -0.25))
                l = max(0, int(x - math.sqrt(n)))
                r = min(int(pow(n, 0.75)), int(x + math.sqrt(n)))

                L = samples[max(1, l - 1)]
                H = samples[r - 1]
                LP = self.rank(list=temp, element=L)
                HP = self.rank(list=temp, element=H)

                p = []
                for num in temp:
                    if L <= num <= H:
                        p.append(num)

                if LP <= self.k <= HP and len(p) <= 4 * pow(n, 0.75) + 1:
                    p = merge.run(p)
                    result[name] = p[self.k-LP]
                    result[name+"_epochs"] = epoch
                    break

        return result
