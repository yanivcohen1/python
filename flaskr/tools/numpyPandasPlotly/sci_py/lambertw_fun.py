from scipy.special import lambertw
import numpy as np

# x*e^x = 4
# W(x*e^x) = W(4)
# x = W(4)
# https://www.youtube.com/watch?v=6x1dUo7S5UE
print("x*e^x = 4 => x = lambertw(4) =", lambertw(4))

# x^x=4
# x*ln(x) = ln(4) , y = ln(x) => x=e^y
# y*e^y = ln(4) => W(y) = W(ln(4))
# y = ln(x) = W(ln(4))
# x = e^W(ln(4)) => x = 2
print("x^x = 4")
x = np.real(np.exp(lambertw(np.log(4))))
print("x = e^W(ln(4)) => x =", x)
print("x^x =", x**x)
print()

# 0.5^x = x
# x ^ 1/x = 0.5
# ln(0.5) = 1/x * ln(x), y = ln(x) => 1/x = 1/e^y = e^-y
# -y*e^-y = -ln(0.5) => W(-y) = W(-ln(0.5))
# W(-ln(x)) = W(-ln(0.5))
# -ln(x) = W(-ln(0.5))
# x = e^-W(-ln(0.5)) =~ 0.641
print("0.5^x = x  => x^1/x = 0.5")
x = np.real(np.exp(-lambertw(-np.log(0.5))))
print("x = e^-W(-ln(0.5)) => x =", x)
print("x^1/x =", x**(1/x))
