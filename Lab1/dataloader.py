class DataLoader:
    """
    加载数据集
    """
    def __init__(self, file_path):
        self.dict = dict()
        for line in open(file_path):
            line = line.strip().split('\t')
            if not self.dict.get(int(line[0])):
                self.dict[int(line[0])] = {int(line[1])}
            else:
                self.dict[int(line[0])].add(int(line[1]))
        # for key in self.dict.keys():
        #     self.dict[key] = sorted(list(self.dict[key]))

    def load(self):
        return self.dict
