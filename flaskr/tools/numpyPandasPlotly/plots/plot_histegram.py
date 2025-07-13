import matplotlib.pyplot as plt
import numpy as np

# Create a random number generator with a fixed seed for reproducibility
rng = np.random.default_rng(19680801)

N_points = 100000
n_bins = 20

# Generate two normal distributions
dist1 = rng.standard_normal(N_points)
dist2 = rng.standard_normal(N_points)

fig, axs = plt.subplots(1, 2, tight_layout=True) # sharey=true -> share y scale, tight_layout -> tight sides space

# We can set the number of bins with the *bins* keyword argument.
axs[0].hist(dist1, bins=n_bins)
axs[1].hist(dist2, bins=n_bins, density='norm', label='norm')

axs[0].set_xlabel("values")
axs[0].set_ylabel("how many")
axs[1].set_xlabel("values")
axs[1].set_ylabel("probility")

plt.show()

# numpy histegram
data = [-0.5, 0.5, 0.5, 0.5,
    1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2]

plt.hist(data, bins=5, range=[-1, 4], histtype='step',edgecolor='r',linewidth=3, ls='dashed')

H, bins = np.histogram(data, bins=5, range=[-1, 4])
# H += np.histogram(data[6:], bins=5,range=[-1, 4])[0]

plt.bar(bins[:-1] - data[0], H, width=1, edgecolor='b', linewidth=3)
plt.plot(bins[:-1] - data[0], H, "k")

plt.show()
