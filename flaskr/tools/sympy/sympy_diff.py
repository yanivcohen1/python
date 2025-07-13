# solve eq -> y"(x) +9y(x) = 0, let y(0) = 1 and y'(0) = 0
# the solution is -> y(x) = cos(3*x)
# https://reference.wolfram.com/language/ref/Plot.html
# in wolframalpha -> y"(x) +9y(x) = 0, y'(0) = 0, y(0) = 1
# in wolframalpha y=cos(3*x) -> plot cos(3*x), x=-1..1
# in wolframalpha -> plot x^2 y^3, x=-1..1, y=0..3
# in wolframalpha -> Plot[y"(x) +9y(x) = 0, y'(0) = 0, y(0) = 1, {x, -3pi, 3Pi}]
# in wolframalpha -> Plot[{Sin[x], Sin[2 x], Sin[3 x]}, {x, 0, 2 Pi}, PlotLegends -> "Expressions"]
from sympy import Function, dsolve, symbols, Eq
import matplotlib.pyplot as plt
import numpy as np

y = Function('y')
x = symbols('x')

# Define the ODE as an equation ( y"(x) = Y'xx = y(x).diff(x, x) )
ode = Eq(y(x).diff(x, x) + 9*y(x), 0)

# Add starting terms to the ODE equation
# For example, let y(0) = 1 and y'(0) = 0.0
# This means that the initial value of y is 1 and the initial value of y' is 0
# To add these starting terms, we use the ics argument of dsolve
ics = {y(0): 1, y(x).diff(x).subs(x, 0): 0.0}

# Solve the ODE using dsolve with the ics argument
y_sol = dsolve(ode, y(x), ics=ics)

# Print the solution
print(y_sol)


# Function to calculate energy numerically
def fill_vals(x_value):
    # Substitute symbolic values with numerical constants
    return (
        y_sol
        .subs({x: x_value})
        .evalf()
    )

x_vals = np.linspace(-10, 10, 100)

y_vals = []
for x_val in x_vals:
    y_val = fill_vals(x_val)
    y_vals.append(y_val.rhs)

plt.plot(x_vals, y_vals, label=f"{y_sol.lhs} = {y_sol.rhs}")
plt.xlabel("x")
plt.ylabel("Y(x)")
plt.title("solve y''(x) +9y(x) = 0, y'(0) = 0, y(0) = 1")
plt.legend()
plt.grid(True)
# Show the plot
plt.show()
