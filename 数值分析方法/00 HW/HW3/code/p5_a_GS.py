from numpy import *
import numpy as np

# 输入矩阵阶数及相关矩阵
n = 3
LU  = np.array([
    [0, -1, 1],
    [0, 0, 2],
    [0, 0, 0]
])
LU = -LU
b = np.array([1, 0, 4])
x0 = np.zeros(3)
D = np.array([
    [3, 0, 0],
    [3, 6, 0],
    [3, 3, 7]
])
# 对D求逆
D_1 = np.linalg.inv(D)

k = 0
Max = 100
TOL = 0.001
# 开始迭代
while(k < Max):
    x = np.matmul(D_1,(np.matmul(LU,x0) + b)) # 注意np.matmul()方法与直接*的区别
    print("x", "%d"%k,"=", x)
    # 设置结束TOL
    if(np.linalg.norm(x - x0, ord = inf) < TOL):
        break;
    x0 = x
    k = k + 1
print("The procedure is successful!")

