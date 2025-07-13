import numpy as np
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt

# https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_bvp.html
# solve eq with missing y'(0)
# y(x)'' + k**2 * y(x) = 0
# y(0) = y(1) = 0
# the solution in y = A * sin(kx), y'(x) = Akcos(kx), for x=0, A=1 => y(0)'= k
# y(1) = cos(k*1) = 0 => k = pi*n

# Define the differential equation as a system of first-order ODEs
def ode_system(x, y, p):
    k = p[0]
    return np.vstack((y[1], -(k**2) * y[0])) # [y', y''], y'' = -k**2 * y


# Boundary conditions: y'(0) = k for A=1, x=0 see above
def bc(ya, yb, p):
    k = p[0]
    y_0 = ya[0]
    y_1 = yb[0]
    y1_0 = ya[1]
    return np.array([y_0-0, y_1-0, y1_0 - k]) # errors = [ya[0]-y(0), yb[0]-y(1), ya[1]-y(0)']


# Initial mesh
x = np.linspace(0, 1, 5) # dt=0.25

# Initial guess for the solution and parameter k
y_guess = np.zeros((2, x.size))
# y(0) = y(1) = 0
# the solution in y = sin(kx)
# one cycle => k=2*pi*n => sin(2 * pi * x)
# y_guess[y_index, x_index]
y_guess[0, 1] = 1 # y1_max(x=2*((1-0)/2) = 0.25) x_index = 0.25/dt = 1
y_guess[0, 3] = -1 # y2_min(x=(3*2*((1-0)/2)) = 0.75) x_index = 0.75/dt = 3

k_guess = []
errors = []

for k in range(1, 10):
    k_gues = np.array([k])

    # Solve the BVP
    sol = solve_bvp(ode_system, bc, x, y_guess, p=k_gues)

    # Verify if the solution was successful
    if sol.success:
      # shooting backwards to the origin (hw6_ex2)
        errors.append(np.abs(k - sol.p[0]))
        k_guess.append(k)
    else:
        print(f"when k={k} The solver did not converge to a solution.")

# plot k Predicted vs Error in Guess
plt.plot(k_guess, errors, marker=".")
plt.xlabel("Predicted k")
plt.ylabel("Error in guess")
plt.title("k Predicted vs Error in Guess")
plt.grid()
plt.show()

# plot the solution at min error for k
x_plot = np.linspace(0, 1, 100)
k = k_guess[np.argmin(errors)]
sol = solve_bvp(ode_system, bc, x, y_guess, p=[k])
y_plot = sol.sol(x_plot)[0]
plt.plot(x_plot, sol.sol(x_plot)[0], label="y = sin(k * x)")
plt.plot(x_plot, sol.sol(x_plot)[1], label="y' = k*cos(k * x)")
plt.title(f"Solution at k={k} where minimum Error in Guess")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()
plt.show()
