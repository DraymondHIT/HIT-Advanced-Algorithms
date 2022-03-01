class Naive:
    def __init__(self, corpus, k):
        self.corpus = corpus
        self.k = k

    @staticmethod
    def merge(list_left, list_right):
        """
        合并有序数组
        """
        l, r = 0, 0
        new_list = []
        while l < len(list_left) and r < len(list_right):
            if list_left[l] <= list_right[r]:
                new_list.append(list_left[l])
                l += 1
            else:
                new_list.append(list_right[r])
                r += 1
        new_list += list_left[l:]
        new_list += list_right[r:]
        return new_list

    def merge_sort(self, mylist):
        """
        归并排序
        """
        if len(mylist) <= 1:
            return mylist

        mid = len(mylist) // 2
        list_left = self.merge_sort(mylist[:mid])
        list_right = self.merge_sort(mylist[mid:])
        return self.merge(list_left, list_right)

    def run(self):
        result = {}
        temp = self.merge_sort(self.corpus["uniform"])
        result["uniform"] = temp[self.k-1]
        temp = self.merge_sort(self.corpus["normal"])
        result["normal"] = temp[self.k-1]
        temp = self.merge_sort(self.corpus["zipf"])
        result["zipf"] = temp[self.k-1]
        return result
