import numpy as np


class DataGenerator:
    """
    加载数据集
    """

    def __init__(self, n):
        self.dict = {"uniform": np.random.uniform(1, 1001, n).astype(np.int).tolist(),
                     "normal": np.random.normal(500, 200, n).astype(np.int).tolist(),
                     "zipf": np.random.zipf(1.2, n).astype(np.int).tolist()}

    def load(self):
        return self.dict
