import sympy as sym

x, y = sym.symbols('x, y')

# Define the equations
eq1 = sym.Eq(x + y, 5) # x + y = 5
eq2 = sym.Eq(x**2 + y**2, 17) # x^2 + y^2 = 17

# Solve the system of equations
result = sym.solve([eq1, eq2], (x, y))

# Print the result [(x, y)]
print(result) # print [(1, 4), (4, 1)]
