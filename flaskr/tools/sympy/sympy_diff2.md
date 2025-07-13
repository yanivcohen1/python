You're absolutely right. Separation of variables isn't always the best approach for every differential equation. In this case, there's a more efficient method to solve this specific equation: characteristic equations. 

Here's how to solve the equation y''(x) + 9y(x) = 0 with characteristic equations:

1. **Rewrite the equation as a homogeneous linear equation:**
The equation is already in this form: y''(x) + 9y(x) = 0.

2. **Assume the solution has the form y(x) = e^(λx):**
This is a common assumption for solving homogeneous linear equations with constant coefficients. λ is an unknown constant to be determined.

3. **Substitute the assumed solution and its derivatives into the equation:**
y(x) = e^(λx)
y'(x) = λ * e^(λx)
y''(x) = λ^2 * e^(λx)

Substitute these into the original equation:
λ^2 * e^(λx) + 9 * e^(λx) = 0

4. **Factor out e^(λx):**
e^(λx) (λ^2 + 9) = 0

Since e^(λx) is never zero (except for x approaching negative infinity), we can ignore it and focus on the remaining part:

λ^2 + 9 = 0

5. **Solve the characteristic equation:**
This is a quadratic equation. Solve for λ:
λ^2 + 9 = 0
λ = ±3i (where i is the imaginary unit)

**6. General solution:**
Since we have two complex roots (imaginary unit multiples of a real number), the general solution for y(x) will be a linear combination of exponential terms with these roots as exponents:
y(x) = C1 * e^(3ix) + C2 * e^(-3ix)

**7. Apply initial conditions to find specific constants (C1 and C2):**
We are given:
y(0) = 1
y'(0) = 0

Apply these conditions to the general solution:
y(0) = C1 * e^(3i*0) + C2 * e^(-3i*0) = C1 + C2 = 1 (since e^(0) = 1)
y'(0) = 3iC1 * e^(3i*0) - 3iC2 * e^(-3i*0) = 3iC1 - 3iC2 = 0 (since e^(0) = 1 and i * (-i) = 1)

Solving this system of equations for C1 and C2, we find:
C1 = C2 = 1/2

**8. Final solution:**
Substitute the values of C1 and C2 back into the general solution:
y(x) = (1/2) * e^(3ix) + (1/2) * e^(-3ix) 
Using Euler's identity:  
y(x) = (1/2) * (cos(3x) + i*sin(3x) + cos(3x) - i*sin(3x))
The final resoult is:
**y(x) = cos(3x)**

**Note:** Due to the presence of imaginary unit multiples in the exponents, the solution involves complex-valued functions. However, depending on the context of your problem, you might be interested in the real and imaginary parts of this solution separately, or it might be necessary to convert it to a trigonometric form using Euler's formula.
