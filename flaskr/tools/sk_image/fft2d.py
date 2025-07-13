# https://scikit-image.org/docs/stable/auto_examples/
import matplotlib.pyplot as plt
import numpy as np
from skimage.data import gravel
from skimage.filters import difference_of_gaussians, window
from scipy.fft import fftn, fftshift

image = gravel()
# Apply a Hann window to reduce edge artifacts (מלאכותי), window = 1/L*sin(2pi/L)^2
wimage = image * window('hann', image.shape)  # window image to improve FFT
# Apply the Difference of Gaussians (DoG) filter (bend wide filter)
# edges->diff = g(σ1)-g(σ2); gaussians = 1/σ*e^-[(x-µ)^2/2σ^2]
filtered_image = difference_of_gaussians(image, 1, 12)
filtered_wimage = filtered_image * window('hann', image.shape) # window image to improve FFT
im_f_mag = fftshift(np.abs(fftn(wimage)))
fim_f_mag = fftshift(np.abs(fftn(filtered_wimage)))

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 7))
ax[0, 0].imshow(image, cmap='gray')
ax[0, 0].set_title('Original Image')
cb1 = ax[0, 1].imshow(np.log(im_f_mag), cmap='magma')
ax[0, 1].set_title('Original FFT Magnitude (log)')
ax[1, 0].imshow(filtered_image, cmap='gray')
ax[1, 0].set_title('Filtered Image')
cb2 = ax[1, 1].imshow(np.log(fim_f_mag), cmap='magma')
ax[1, 1].set_title('Filtered FFT Magnitude (log)')
plt.colorbar(cb1)
plt.colorbar(cb2)
plt.tight_layout()
plt.show()
