# numba types
# https://numba.pydata.org/numba-doc/dev/reference/types.html
import numpy as np
from numba import jit, objmode
import pandas as pd
import time

# Create a NumPy array (avoid dtype=object)
A = np.array([[2, 5], [4, 5], [0, 8], [6, 7], [1, 8], [0, 1], [1, 3], [1, 3], [2, 4]], dtype=np.int32)
B = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=int)

data = [1., 2., 3., 4., 5., 6., 7., 8., 9.]

# Define a function to optimize with Numba
@jit(nopython=True)
def f(A: np.ndarray, B: np.ndarray, C: float) -> np.ndarray:
    result = np.zeros(len(B), dtype=float)  # Initialize an array to store results
    for i in range(len(B)):
        result[i] = g(A[i], B) + C
    return result

def callback_panda_debug(a):
    # This code is executed by the interpreter.
    b = a.reshape(-1)# same as .flatten()
    c = b[:2]
    df = pd.DataFrame(data, columns=['Numbers'])
    res = np.vstack((c , np.asarray(df['Numbers'])[:2]))
    res1 = res + a[:2]
    return np.asarray(res1, np.float32)

# Define another function (simplified representation of your actual function)
@jit(fastmath=True)
def g(a: np.ndarray, B: np.ndarray) -> float:
    # Some function of 'a' and 'B'
    with objmode(y= 'float32[:,:]'):  # annotate return type float32 2d arry
        # this region is executed by object-mode.
        y = callback_panda_debug(A)
    return 19.12 / (len(a) + len(B) + sum(y[0, :]))

# Call the optimized function
start = time.time()
result = f(A, B, 5.0)
print("Result:", result)
print(f'run toke {time.time()-start:.2f} sec')
