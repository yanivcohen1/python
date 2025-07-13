import matplotlib.pyplot as plt
import numpy as np

x_d = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
y_d = np.array([0, 0.8, 0.9, 0.1, -0.6, -0.8, -1, -0.9, -0.4])

plt.figure(figsize = (12, 6))
for i in range(1, 7):

    # get the polynomial coefficients
    y_est = np.polyfit(x_d, y_d, i)
    plt.subplot(2,3,i)
    plt.plot(x_d, y_d, 'o')

    # print poly
    formula = ""
    for j in range(i + 1):
        formula += f'{"+" if y_est[j]>=0 else ""}'
        if i-j == 0:
            formula += f'{y_est[j]:.2f}'
        else:
            formula += f'{y_est[j]:.2f}*X^{i-j} '
    print(f"poly {i}: {formula}")

    # evaluate the values for a polynomial
    plt.plot(x_d, np.polyval(y_est, x_d), label=formula)
    np.set_printoptions(precision=2)
    if i > 3:
        plt.title(f'Polynomial order {i} \n {y_est[:4]} ...')
    else:
        plt.title(f'Polynomial order {i} \n {formula}')
    if i == 1:
        f = lambda X: y_est[0]*X**1 + y_est[1]
        plt.plot(x_d, f(x_d), ".")
        plt.title(f'Polynomial order {i}: \n {y_est[0]:.2f}*X^1 + {y_est[1]:.2f}')

plt.tight_layout()
plt.show()
