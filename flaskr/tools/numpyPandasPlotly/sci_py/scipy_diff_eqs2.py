# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
# https://apmonitor.com/pdc/index.php/Main/SolveDifferentialEquations
# https://www.youtube.com/watch?v=QlRB2k9i4gc
# solve: y''(t) + b*y'(t) + c*sin(y(t)) = 0
# we define: dy = y'(t)
# and:       dy2 = y''(t) = -b*dy(t) - c*sin(y(t))

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t = np.linspace(0, 10, 101)    # timeline: delta(t)/2 - points
y0 = [np.pi - 0.1, 0.0]  # [y0, y'0] initial values
B = 0.25
C = 5.0

def dydt_fun(z, t, b, c):
    y, dy = z # same order as init vals
    dydt = dy
    dy2dt = -b*dydt - c*np.sin(y)
    return [dydt, dy2dt] # same order as init vals

sol = odeint(dydt_fun, y0, t, args=(B, C))

plt.plot(t, sol[:, 0], 'b', label='y(t)')
plt.plot(t, sol[:, 1], 'g', label='y\'(t)')
plt.legend(loc='best')
plt.xlabel('t')
plt.grid()
plt.show()
