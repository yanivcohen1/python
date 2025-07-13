# solve PDE Heat Equation: ∂u/∂t ​= κ*∂²𝑢/∂x² # pylint: disable=E2515
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Set up initial conditions and parameters
N = 100  # Number of spatial points
x = np.linspace(0, 1, N)
dx = x[1] - x[0] # (1-0)/N
y0 = np.sin(np.pi * x)  # Initial condition
t_span = [0, 1]

# Define the PDE as a system of ODEs using the method of lines
# Define the Heat equation as a system of first-order ODEs
def pde_system(t, y, N):
    dydt = np.zeros_like(y)
    # Discretized Laplacian base on "Central difference Approximating Derivatives"
    # Discretized Laplacian | x=x_i: (u_{i-1}-2u_i+u_{i+1}) / dx^2
    dydt[1:-1] = (y[:-2] - 2*y[1:-1] + y[2:]) / dx**2  # Discretized Laplacian
    return dydt

# Solve the PDE - defalt RK45 Runge-Kutta method of order 5(4)
solution = solve_ivp(lambda t, y: pde_system(t, y, N), t_span, y0, method='RK45')

# Plot the results
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
X, T = np.meshgrid(x, solution.t)
ax.plot_surface(X, T, solution.y.T, cmap='viridis')

# Set labels and show the plot
ax.set_xlabel('Position - Spatial coordinate')
ax.set_ylabel('Time')
ax.set_zlabel('Temperature')
plt.title("Temperature T(x,t) by solve PDE Heat Equation: \n \
            ∂u/∂t ​= κ*∂²u/∂x²;  T0=sin(pi * x)")
plt.show()
