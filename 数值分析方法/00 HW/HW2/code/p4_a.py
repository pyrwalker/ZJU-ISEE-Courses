import math
from sympy import *


x1 = symbols('x1')
x2 = symbols('x2')
x3 = symbols('x3')

gfun =  (15 * x1 + x2 * x2 - 4 * x3 - 13) * (15 * x1 + x2 * x2 - 4 * x3 - 13) +\
        (x1 * x1 + 10 * x2 - x3 - 11) * (x1 * x1 + 10 * x2 - x3 - 11) +\
        (x2 * x2 * x2 - 25 * x3 + 22) * (x2 * x2 * x2 - 25 * x3 + 22)


grad_1 = diff(gfun, x1)
grad_2 = diff(gfun, x2)
grad_3 = diff(gfun, x3)

epsilon = 0.001


x1_value = 0
x2_value = 0
x3_value = 0

iter_cnt = 0
current_step_size = 10000 

grad_1_value = (float)(grad_1.subs({x1:x1_value, x2: x2_value, x3:x3_value}).evalf())
grad_2_value = (float)(grad_2.subs({x1:x1_value, x2: x2_value, x3:x3_value}).evalf())
grad_3_value = (float)(grad_3.subs({x1:x1_value, x2: x2_value, x3:x3_value}).evalf())  

current_obj = gfun.subs({x1: x1_value, x2: x2_value, x3:x3_value}).evalf()

while(abs(grad_1_value) + abs(grad_2_value) >= epsilon):  
    iter_cnt += 1


    t = symbols('t')
    x1_updated = x1_value + grad_1_value * t
    x2_updated = x2_value + grad_2_value * t
    x3_updated = x3_value + grad_3_value * t
    gfun_updated = gfun.subs({x1: x1_updated, x2: x2_updated, x3: x3_updated})
    grad_t = diff(gfun_updated, t)
    t_value = solve(grad_t, t)[0] 


    grad_1_value = (float)(grad_1.subs({x1: x1_value, x2: x2_value, x3: x3_value}).evalf()) 
    grad_2_value = (float)(grad_2.subs({x1: x1_value, x2: x2_value, x3: x3_value}).evalf()) 
    grad_3_value = (float)(grad_3.subs({x1: x1_value, x2: x2_value, x3: x3_value}).evalf())     
    x1_value = (float)(x1_value + t_value * grad_1_value)
    x2_value = (float)(x2_value + t_value * grad_2_value) 
    x3_value = (float)(x3_value + t_value * grad_3_value)

    current_obj = gfun.subs({x1: x1_value, x2: x2_value, x3: x3_value}).evalf()
    current_step_size = t_value

    print('itCnt: %2d  cur_point (%3.2f, %3.2f, %3.2f) step_size : %5.4f' % (iter_cnt, x1_value, x2_value, x3_value, current_step_size)) 
    