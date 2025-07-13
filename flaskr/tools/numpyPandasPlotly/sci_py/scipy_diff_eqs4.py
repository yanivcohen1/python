# solve eq -> y"(x) + k*y(x) = 0, where k: 0 < k < 1
# let init y(0) = 1 and y'(0) = 0
# the solution is -> y(x) = cos(3*x) when k=9

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the differential equation as a system of first-order equations
def dydx_fun(z, x, k):
    y = z[0] # y  # same order as init vals
    dy = z[1] # y' # same order as init vals
    dydx = dy # y' = dy/dx
    dy2dx = -k * y # y'' = -9y
    return [dydx, dy2dx] # same order as init vals

# Define the initial conditions
y0 = [1, 0] # y(0) = 1, y'(0) = 0

# Define the range of x values
t = np.linspace(-10, 10, 100)

# solve ODEs
k = 0.1
y1 = odeint(dydx_fun,y0,t,args=(k,))
k = 0.5
y2 = odeint(dydx_fun,y0,t,args=(k,))
k = 0.9
y3 = odeint(dydx_fun,y0,t,args=(k,))

# plot results
plt.plot(t,y1.T[0],'r-',linewidth=2,label='k=0.1')
plt.plot(t,y2.T[0],'b--',linewidth=2,label='k=0.5')
plt.plot(t,y3.T[0],'g:',linewidth=2,label='k=0.9')
plt.xlabel('time')
plt.ylabel('y(t)')
plt.legend()
plt.grid()
plt.show()
