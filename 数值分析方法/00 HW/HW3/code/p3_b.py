import numpy as np
from numpy import *
# 给定输入
n = 3 # 3*3的矩阵
a = np.array([
    [3.03, -12.1, 14, -119],
    [-3.03, 12.1, -7, 120],
    [6.11, -14.2, 21, -139]
])
# print(a)


for i in range(0,n):
    list = a[i:,i]
    # 找到非零最小值的下标
    [[k]]= np.where(list == np.min(np.abs(list[np.nonzero(list)])))
    p = k + i # 避免了前i行的影响
    # 进行行变换
    if(p != i):
        a[[i,p],:] = a[[p,i],:]
    # 消去第i列元素
    for j in range (i+1, n):
        m = a[j][i] / a[i][i]
        a[j] = a[j] - m * a[i]
        print(a)

#根的唯一性判定 
if(a[n-1][n-1] == 0):
    print('no unique soulution exists')
    input()# 停止程序继续进行

xn = a[n-1][n] / a[n-1][n-1]
X = [xn]

# 求根并放入列表X
for k in range(n-2, -1, -1):
    b=0
    cnt = 0
    for j in range(k+1,n):
        b = b + a[k][j] * X[-1-cnt]
        cnt += 1
    x = (a[k][n] - b) / a[k][k]
    X.append(x)
# 反转列表
X.reverse()    
print(X)