# f(x, y) = x² + y² - 10.0 = 0
# g(x, y) = x + y + k = 0 ; for k: 0 <= k <= 4
# You should get x = 0.1583124, y = -3.1583124, whene k = 3
# for k=0 you should get:  x = 2.23606798, y = -2.23606798
# if you start with x = y = 1 as an initial guess.
from scipy.optimize import fsolve

def h(z, k):
    x, y = z
    f = x**2 + y**2 - 10.0
    g = x + y+ 1*k
    return [f,g]

init_gess = [1,1]
for k in range(0, 5, 2):
    res = fsolve(h, init_gess, args=(k), maxfev=5000)
    print(f"for k={k}: ", res)
    # Verify the solution is a root
    result = h(res, k)
    print(f"validated if fun(root)=0 find:", result) # result= [0.]
# the output is [x_root, y_root]:
# for k=1:  [-2.67944947  1.67944947]
# for k=2:  [ 1. -3.]
# for k=3:  [ 0.1583124 -3.1583124]
