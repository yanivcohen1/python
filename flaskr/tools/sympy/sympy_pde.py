from sympy import Function, Eq, pde_separate_mul, Derivative as D, dsolve, symbols, lambdify
from sympy.abc import x, y
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the unknown function
u = Function('u')

# Define the PDE: U"(x, y)xx = U"(x, y)yy
eq = Eq(D(u(x, y), x, x), D(u(x, y), y, y))

# Perform separation of variables
X, Y = map(Function, 'XY')
X_part, Y_part = pde_separate_mul(eq, u(x, y), [X(x), Y(y)])

# Solve the ODEs for X and Y with initial conditions
X_ode = Eq(D(X(x), x, x) - symbols('lambda')*X(x), 0)
Y_ode = Eq(D(Y(y), y, y) - symbols('lambda')*Y(y), 0)

# Define initial conditions
initial_conditions = {X(0): 1, Y(0): 1}  # Example initial conditions

# Solve the ODEs with initial conditions
X_sol = dsolve(X_ode, X(x), ics={X(0): initial_conditions[X(0)]})
Y_sol = dsolve(Y_ode, Y(y), ics={Y(0): initial_conditions[Y(0)]})

# Assuming a multiplicative constant 'A' for the solutions
A = symbols('A')
u_solution = A * X_sol.rhs * Y_sol.rhs
print(u_solution)

# Convert symbolic expressions to numerical functions
u_lambdified = lambdify((x, y), u_solution.subs(A, 1).subs('lambda', -1)
                        .subs('C2', 1))

# Create a grid and compute the numerical values of u(x, y)
x_vals = np.linspace(-5, 5, 100)
y_vals = np.linspace(-5, 5, 100)
X_vals, Y_vals = np.meshgrid(x_vals, y_vals)
Z_vals = u_lambdified(X_vals, Y_vals)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X_vals, Y_vals, Z_vals, cmap='viridis')

# Set labels and show the plot
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('u(x, y)')
ax.grid(True)
plt.show()
