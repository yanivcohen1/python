import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Define the wave equation as a system of first-order ODEs
# solve wave equation: ∂²y \ ∂t² = c² * ∂²y \ ∂x²
def wave_eq(t, y, c, N):
    d2ydt2 = np.zeros_like(y)
    # Discretized Laplacian base on "Central difference Approximating Derivatives"
    # Discretized Laplacian | x=x_i: (y_{i-1}-2y_i+y_{i+1}) / dx^2
    d2ydt2[1:-1] = c**2 * (y[:-2] - 2*y[1:-1] + y[2:]) / dx**2
    return d2ydt2

# Parameters
c = 1.0  # Wave speed
L = 10   # Length of the domain
N = 100  # Number of spatial points
dx = L / (N - 1)
x = np.linspace(0, L, N)

# Initial conditions
y0 = np.sin(np.pi * x / L)
y0[0], y0[-1] = 0, 0  # Boundary conditions: u(0,t) = u(L,t) = 0
v0 = np.zeros_like(x)  # Initial velocity

# Combine initial conditions into a single state vector
initial_state = np.concatenate([y0, v0])

# Time span
t_span = (0, 10)

# Solve the wave equation
sol = solve_ivp(wave_eq, t_span, initial_state, args=(c, N) , method='RK45')

# Extract the solution
u = sol.y[:N, :]  # Displacement
v = sol.y[N:, :]  # Velocity (u')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a meshgrid for the plot
T, X = np.meshgrid(sol.t, x)

# Plot the 3D surface
ax.plot_surface(X, T, u, cmap='viridis')

# Set labels
ax.set_xlabel('Position')
ax.set_ylabel('Time')
ax.set_zlabel('Displacement')
plt.title("Wave y(x,t) by solve PDE Wave Equation:\n \
  ∂²y \ ∂t² = c² * ∂²y \ ∂x²;  T0 = sin(pi * x)")

plt.show()
