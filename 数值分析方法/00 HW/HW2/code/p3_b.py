import numpy as np
from numpy.linalg import solve
import math

x = np.zeros(3).reshape(3)
# print(x)
print('x0 = ',x)

for i in range(1,100):
    F = np.array(
        [x[0]*x[0]+x[1]-37,
        x[0]-x[1]*x[1]-5,
        x[0]+x[1]+x[2]-3]
    )
    # print(F)

    J = np.array([
        [2*x[0]],[1],[0],
        [1],[-2*x[1]],[0],
        [1],[1],[1]

    ]).reshape(3,3)
    # print(J)
    y = solve(J,-F)
    # print(y)
    x = x + y
    print('x%d = '%i,x)