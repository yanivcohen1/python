# https://apmonitor.com/pdc/index.php/Main/SolveDifferentialEquations
# https://www.youtube.com/watch?v=QlRB2k9i4gc
# T: Tempurter, t: time
# dT2t = dT^2/dt = -(3.083e8*np.exp(-56000/(8.314*T0))*dTt*0.033)
# dTt = dT/dt = (0.45*-98000*dT2t+5.7431*(273.15-T0))/(2018.94)
# My initial values are:
# T[0]= T0 = 281.15
# T'[0]= dT0 = 6.529

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

t = np.linspace(0, 1800, 901)    # timeline: delta(t)/2 - points
T0 = [281.15, 6.529]  # initial values

def df(c, t):
    Temp = c[0] # same order as init vals
    dT = c[1] # same order as init vals
    Tdt = -(3.083e8*np.exp(-56000/(8.314*Temp))*dT*0.033)
    dTdt = (0.45*-98000*Tdt + 5.7431*(273.15 - Temp))/(2018.94)
    return [dTdt, Tdt] # same order as init vals

sol = odeint(df, T0, t)

plt.plot(t, sol[:,0] - 273.15, label='T')
# plt.plot(t, sol[:,1], label='T\'')
plt.xlabel('t (sec)')
plt.ylabel('T (degrees C)')
plt.grid()
plt.legend()
plt.title("Temperature over time")
plt.show()
