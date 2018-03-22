import numpy as np
a_list = list(range(10))
b_list = np.array(a_list)
c_list = np.zeros(10, dtype=int)
two_dimension = np.zeros((4,4), dtype=int)
d_list = np.ones((4,4), dtype=float)
e_list = np.full((4,4),3.14)

print(c_list)
a = np.random.random((3,3)) #生成一个随机数的矩阵
b = np.random.randint(0,10,(3,3))
c = np.arange(2,18,2)
d = e_list[:1,:1]
print(d)