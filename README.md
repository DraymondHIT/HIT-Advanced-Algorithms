# HIT-Advanced-Algorithms
哈工大2022春高级算法（本科）课程实验

### 实验一 用minHash实现集合的相似性连接

#### 实验内容

分别实现两重循环算法和minHash方法求解如下计算问题，利用教师发布在教学QQ群中的三个公开实验数据集(AOL, DILICIOUS, LINUX)开展对比实验和扩展性实验，观察Hash函数个数对算法性能的影响，并根据实验结果讨论经验参数设置办法。

**输入**：集族$R=\{r_1,r_2,\dots,r_n\}$，实数$c \in(0,1]$

**输出**：$\{<r,s>|r,s\in R,|r \cap s|/|r \cup s|\geq c\}$

