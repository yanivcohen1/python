# integral ∫[0, x](sin(x)dx)
import numpy as np
from scipy.integrate import quad
from scipy.integrate import cumtrapz
import matplotlib.pyplot as plt

x = np.arange(0, np.pi, 0.01)
F_exact = -np.cos(x)
F_approx = cumtrapz(np.sin(x), x)

plt.figure(figsize = (10,5))
plt.plot(x, F_exact)
plt.plot(x[1::], F_approx)
plt.grid()
# plt.tight_layout()
plt.title('$F(x) = \int_0^{x} sin(y) dy$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend(['Exact with Offset', 'Approx'])
plt.show()
