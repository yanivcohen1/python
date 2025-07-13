import numpy as np
import matplotlib.pyplot as plt

def f(t, y):
    # Define the vector-valued function f(t, y)
    # y"(t) - t*y'(t) + 3*y(t) = 0
    # y"(t) = t*y'(t) - 3*y(t)
    # y[1] = y' ; y[0] = y
    # return np.array([y[1], t + y[1] - 3 * y[0]]) # [y', y'']

    # y"(t) + y(t) = 0 , y(0)=2, y'(0)=1
    return [y[1], -y[0]] # [y', y'']

# Euler method for solving ODEs y[0]]) # [y', y'']
def euler(f, tv, y0, N):
    t0, T = tv
    h = (T - t0) / N
    ts = np.zeros(N + 1)
    ys = np.zeros((N + 1, len(y0)))
    t, y = t0, y0

    ts[0] = t
    ys[0, :] = y

    for i in range(N):
        slop = f(t, y)  # Evaluate direction field at current point
        y_next = y + np.array(slop) * h  # Update y using Euler method
        t = t + h
        ts[i + 1] = t
        ys[i + 1, :] = y_next
        y = y_next

    return ts, ys

# Initial conditions and parameters
t0 = 0
T = 8  # Final time
y0 = np.array([2, 1])  # Initial vector [y1, y2]
N = 5000  # Number of steps

# Solve the ODE using Euler method
ts, ys = euler(f, [t0, T], y0, N)
yfinal = ys[-1, :]

# Print the final values
print(f"y(T) = {yfinal[0]:.5f}, y'(T) = {yfinal[1]:.5f}")

y_exact = np.sin(ts) + 2*np.cos(ts)

# Plot the solution
plt.plot(ts, ys[:, 0], 'b', label='y(t)') # y' = ys[:, 1]
plt.plot(ts, y_exact, 'r--', label="The exact solution is y = sin(t) + 2*cos(t)")
plt.title("Solution y''(t) + y(t) = 0 with y(0)=2, y'(0)=1")
plt.ylabel('y(t)')
plt.xlabel('t')
plt.grid(True)
plt.legend()
plt.show()
