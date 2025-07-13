from sympy import symbols, integrate, exp, sin
from sympy import symbols, Eq, integrate, solve, dsolve, simplify
import sympy as sp
# Define the symbols
x = symbols('x')

# Define the equation with the integral(x^2)=10
equation = Eq(integrate(x**2, x), 10)
sp.pprint(equation)

# Solve the equation x^3/3=10 for 3 solutions
solution = solve(equation, x)

print(solution)
for sol in solution:
    print(sp.re(sol), ",", sp.im(sol))
