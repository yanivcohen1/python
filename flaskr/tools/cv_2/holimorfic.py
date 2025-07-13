import numpy as np
import cv2
from matplotlib import pyplot as plt
# from scipy.fft import fft, ifft, fft2, ifft2

gray_img = cv2.imread('flaskr/tools/cv_2/holimorfic.png', cv2.IMREAD_GRAYSCALE)
#Load the image 'me2.jpg' in grayscale
# gray_img = cv2.imread(r'C:\pyProj\yaniv\test\holimorfic.png', 0) # Read the image in grayscale
#Homomorphic filter function
def homomorphic_filter(image, d0=20, rL=0.5, rH=0.5):
    #Convert the image to logarithmic space
    img_log = np.log1p(np.array(image, dtype="float"))
    # Perform Fourier transform
    dft = np.fft.fft2(img_log)
    dft_shift = np.fft.fftshift(dft)
    #Get the image dimensions
    rows, cols= image.shape
    crow, ccol = rows // 2, cols // 2
    #Create a mask for filtering
    mask = np.ones((rows, cols), dtype=np.float32)
    for i in range(rows):
        for j in range(cols):
            d = np.sqrt((i - crow)**2 +(j - ccol)**2)
            mask[i, j] = (rH-rL) * (1 - np.exp(-((d**2) / (d0**2)))) + rL
    #Apply the filter to the fre frequency image
    dft_shift = dft_shift * mask
    #Perform the inverse Fourier transform
    dft_ishift = np.fft.ifftshift(dft_shift)
    img_back = np.fft.ifft2(dft_ishift)
    img_back = np.abs(img_back)
    #Convert back from logarithmic space
    img_homomorphic = np.expm1(img_back) # Exponential transformation
    #Normalize the result for displaying
    img_homomorphic = cv2.normalize(img_homomorphic, None, 0, 255, cv2.NORM_MINMAX)
    img_homomorphic = np.uint8(img_homomorphic)
    return img_homomorphic
#Apply the homomorphic filter to the image
filtered_image = homomorphic_filter(gray_img)
#Display the original and filtered images
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(gray_img, cmap='gray'), plt.title('Original')
plt.subplot(122), plt.imshow(filtered_image, cmap='gray'), plt.title('Homomorphic Filter')
plt.show()
