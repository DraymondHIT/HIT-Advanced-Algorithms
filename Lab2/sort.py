class MergeSort:
    def __init__(self):
        pass

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

    def run(self, mylist):
        """
        归并排序
        """
        if len(mylist) <= 1:
            return mylist

        mid = len(mylist) // 2
        list_left = self.run(mylist[:mid])
        list_right = self.run(mylist[mid:])
        return self.merge(list_left, list_right)
