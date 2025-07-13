from skimage import color
from skimage import io
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fft2, ifft2
import numpy as np

img_load = io.imread('flaskr/tools/numpyPandasPlotly/sci_py/2d_image_flower.PNG')
rgb_img = color.rgba2rgb(img_load)
gray_img = color.rgb2gray(rgb_img)
# plt.imshow(gray_img, cmap='gray')
# plt.show()

fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(8, 7))

ax[0,0].imshow(gray_img, cmap='gray')
ax[0,0].set_title(f'original image')

# fft in 2D
fft_image = fft2(gray_img)
fy = np.fft.fftfreq(gray_img.shape[0],d=10) #suppose the spacing between pixels is 10mm, for example
fx = np.fft.fftfreq(gray_img.shape[1],d=10)
print('{:.2f} correponds to fx={:.6f} and fy={:.6f}'.format(fft_image[10,20], fx[20], fy[10]))

p1 = ax[0,1].imshow(np.log1p(np.abs(fft_image)), cmap='gray')
ax[0,1].set_title('fft image')
# plt.imshow(np.abs(img_FT), cmap='gray', vmax=50)
# plt.colorbar()
# plt.show()

# Remove low frequencies
th = 5 # threshole
img_FT_alt = np.copy(fft_image)
img_FT_alt[-th:] = 0
img_FT_alt[:,-th:] = 0
img_FT_alt[:th] = 0
img_FT_alt[:,:th] = 0
# inverse fft in 2D

# low pass filter
p2 = ax[1,1].imshow(np.log1p(np.abs(img_FT_alt)), cmap='gray')
ax[1,1].set_title('fft lp filterd image')

img_alt = np.abs(ifft2(img_FT_alt))
ax[1,0].imshow(img_alt, cmap='gray')
ax[1,0].set_title(f'lp filterd image')

# hith pass filter
img_FT_alt = np.copy(fft_image)
th = 5 # threshole
img_FT_alt[-th:] = 0
img_FT_alt[:,-th:] = 0
img_FT_alt[:th] = 0
img_FT_alt[:,:th] = 0
hp_fft_image = fft_image - img_FT_alt
p3 = ax[2,1].imshow(np.log1p(np.abs(hp_fft_image)), cmap='gray')
ax[2,1].set_title('fft hp filterd image')

img_alt = np.abs(ifft2(hp_fft_image))
ax[2,0].imshow(img_alt, cmap='gray')
ax[2,0].set_title(f'hp filterd image')

# plt.imshow(img_alt, cmap='gray')
# plt.colorbar()
plt.colorbar(p1)
plt.colorbar(p2)
plt.colorbar(p3)
plt.tight_layout()
plt.show()
