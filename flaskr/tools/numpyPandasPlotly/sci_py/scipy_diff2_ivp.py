import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Second-order ODE (harmonic motion)
# y''(t) = -ω^2 * y(t) ; y(0) = 1 y(0)'= 0
# solution is: y(t) = cos(2t)
# Convert to first-order system
def second_order_ode(t, z, w):
    y , dy = z # same order as init vals
    dydt = dy
    d2ydt = -(w**2) * y
    return np.array([dydt, d2ydt]) # same order as init vals

# Angular frequency
W = 2

# Initial conditions
y0 = np.array([1, 0])  # Initial position (1) and velocity (0)

# Time span
t_span = (0, 10)

# Solve the ODE
sol = solve_ivp(second_order_ode, t_span, y0, args=(W,), t_eval=np.linspace(0, 10, 101))

# Extract solution components (position and velocity)
t = sol.t
y = sol.y[0]  # Position
v = sol.y[1]  # Velocity (y')

plt.plot(t, y, label="y(t) = cos(2t)")
plt.xlabel("t")
plt.ylabel("y")
plt.title("y(t) by solve Harmonic Motion: y''(t) = -ω^2 * y(t)")
plt.legend()
plt.grid()
plt.show()
