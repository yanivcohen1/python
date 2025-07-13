# https://www.youtube.com/watch?v=slbZ-SLpIgg
import numpy as np
import matplotlib.pyplot as plt

num_sims = 1_000_000 # number of trays

A = np.random.uniform(1, 5, num_sims) # uniform prabbility between 1 to 5 hours
B = np.random.uniform(2, 6, num_sims) # uniform prabbility between 2 to 6 hours

duration = A + B # probbility of a and b (finish A and then finish B)
finish_time = 9 # in hours

plt.figure()
plt.hist(duration, density = True, edgecolor='white')
plt.axvline(finish_time, color='r')
# sum of bools ((duration > finish_time).sum())
res = (duration > finish_time).sum()/num_sims * 100 # precentages for above finish_time
plt.title(
f'''the probbility of a and b done in exactly {finish_time} hours
for above {finish_time} hours is: {res:.2f}% and for under is {(100-res):.2f}%''')
plt.show()
