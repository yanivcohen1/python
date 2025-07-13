from sympy import symbols, Eq, Function
from sympy.solvers.ode.systems import dsolve_system

import matplotlib.pyplot as plt
import numpy as np

f, g = symbols("f g", cls=Function)
x = symbols("x")
# f(x)'= g(x), g(x)'= f(x), f(0)=1, g(0)=0
eqs = [Eq(f(x).diff(x), g(x)), Eq(g(x).diff(x), f(x))]
funcs = [f(x), g(x)]
eqs_sol = dsolve_system(eqs, funcs=funcs, ics={f(0): 1, g(0): 0})
eqs_sol = eqs_sol[0]

# Print the solutions
print(eqs_sol[0].lhs, "=", eqs_sol[0].rhs)
print(eqs_sol[1].lhs, "=", eqs_sol[1].rhs)


# Function to calculate energy numerically
def fill_vals(x_value, i):
    # Substitute symbolic values with numerical constants
    return (
        eqs_sol[i]
        .subs({x: x_value})
        .evalf()
    )

x_vals = np.linspace(-10, 10, 100)

for i, eqs_sol_i in enumerate(eqs_sol):
    y_vals = []
    for x_val in x_vals:
        y_val = fill_vals(x_val, i)
        y_vals.append(y_val.rhs)
    plt.plot(x_vals, y_vals, label=f"{eqs_sol_i.lhs} = {eqs_sol_i.rhs}")

plt.xlabel("x")
# plt.ylabel("Y(x)")
plt.title("solve f(x)'= g(x), g(x)'= f(x), f(0)=1, g(0)=0")
plt.legend()
plt.grid(True)
# Show the plot
plt.show()
