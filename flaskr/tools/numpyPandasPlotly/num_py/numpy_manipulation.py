import numpy as np

a = np.array([1, 2])
a1 = np.vstack((a, [3, 4])) # [[1, 2], [3, 4]]
x, y = a1.T # x =[1,3], y=[2,4]
print('x =', x, ', y =', y) # x =[1,3], y=[2,4]


# equvalent in python native
a = [[1, 2]]
a.append([3, 4]) # [[1, 2], [3, 4]]
x, y = zip(*a) # x =[1,3], y=[2,4]
print('x =', list(x), ', y =', y) # x =[1,3], y=[2,4]
