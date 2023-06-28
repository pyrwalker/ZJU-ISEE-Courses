import numpy as np
from numpy.linalg import solve
import math


x = np.zeros(3).reshape(3)
# print(x)
print('x0 = ',x)
for i in range(1,100):
    F = np.array(
        [3*x[0]-math.cos(x[1]*x[2])-1/2,
        4*x[0]*x[0]-625*x[1]*x[1]+2*x[1]-1,
        math.exp(-x[0]*x[1])+20*x[2]+(10*math.pi-3)/3]
    )
    # print(F)

    J = np.array([
        [3],[x[2]*math.sin(x[1]*x[2])],[x[1]*math.sin(x[1]*x[2])],
        [8*x[0]],[-1250*x[1]+2],[0],
        [-x[1]*math.exp(-x[0]*x[1])],[-x[0]*math.exp(-x[0]*x[1])],[20]

    ]).reshape(3,3)
    # print(J)
    y = solve(J,-F)
    # print(y)
    x = x + y
    print('x%d = '%i,x)