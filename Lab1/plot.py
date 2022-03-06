import numpy as np
import matplotlib.pyplot as plt

## 此文件主要用于根据c选择合适的LSH算法参数

b = 20
r = 2

x = np.linspace(0, 1, 100).tolist()
y = [1 - pow((1 - pow(i, r)), b) for i in x]

plt.plot(x, y)
plt.show()
