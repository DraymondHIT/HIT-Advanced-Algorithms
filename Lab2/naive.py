from sort import MergeSort


class Naive:
    def __init__(self, corpus, k):
        self.corpus = corpus
        self.k = k

    def run(self, name_list):
        result = {}
        merge = MergeSort()
        for name in name_list:
            temp = merge.run(self.corpus[name])
            result[name] = temp[self.k-1]
        return result
