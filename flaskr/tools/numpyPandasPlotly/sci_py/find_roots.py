import numpy as np
from scipy import optimize
# compute the root of f(x)=cos(x)−x
# where x is near −2
f = lambda x: np.cos(x) - x
r = optimize.fsolve(f, -2, maxfev=1000)# look for root in area of x=-2, in 1000 trays
print("r =", r) # r = [0.73908513]
# Verify the solution is a root
print(f"validated root f({r})=", f(r)) # result= [0.]

#---------------------------------------------------------------------
# compute the root of f(x)=1/x
f = lambda x: np.sin(x)-0.5
res = optimize.least_squares(f, (-1,), bounds=(-1, 1)) # bounds ia the area to look roots
print("r =", res.x)
print(f"validated root f({res.x})=", f(res.x))
print(res.message)
