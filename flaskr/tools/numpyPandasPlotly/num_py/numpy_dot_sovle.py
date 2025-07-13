import numpy as np

def dot(A, B):
    N = len(A)
    M = len(A[0])
    P = len(B[0])
    # Pre-fill the result matrix with 0s.
    # The size of the result is 3 x 4 (N x P).
    result = []
    # for i in range(N):
    #     row = [0] * P
    #     result.append(row)
    result = np.zeros((N, P))

    for i in range(N):
        for j in range(P):
            for k in range(M):
                result[i][j] += A[i][k] * B[k][j]
    # for r in result:
    #     print(r)

    return result

# Define vectors a and b
A = np.array([  [2, 0], 
                [1, 9]])
B = np.array([  [3, 9], 
                [4, 7]])

product = A @ B
print("dot:\n", product, "\n")

x = dot(A, B)
print("dot fun:\n", product, "\n")

x = np.linalg.solve(A, B)
print("solve B:\n", A @ x, "\n")

print("B:\n", B, "\n")
