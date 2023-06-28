from numpy import *
import numpy as np

# 输入矩阵阶数及相关矩阵
n = 3
LU  = np.array([
    [0, 1, -1],
    [-1, 0, 1],
    [2, 2, 0]
])
LU = -LU
b = np.array([5, -4, 1])
x0 = np.zeros(3)
D = np.array([
    [4, 0, 0],
    [0, 3, 0],
    [0, 0, 5]
])
# 对D求逆
D_1 = np.linalg.inv(D)

k = 0
Max = 100
TOL = 0.000001
# 开始迭代
while(k < Max):
    x = np.matmul(D_1,(np.matmul(LU,x0) + b)) # 注意np.matmul()方法与直接*的区别
    print("x", "%d"%k,"=", x)
    # 设置结束TOL
    if(np.linalg.norm(x - x0, ord = 2) < TOL):
        break;
    x0 = x
    k = k + 1
print("The procedure is successful!")

