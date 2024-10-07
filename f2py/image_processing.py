import os
import time
import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt

import mf_mixed



import numpy as np
from numpy.lib.stride_tricks import as_strided

def blur_filter_vectorized(image, kernel_size=3):
    # Create the kernel
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
    
    # Get dimensions
    i_height, i_width = image.shape
    k_height, k_width = kernel.shape
    
    # Pad the image
    pad_height = k_height // 2
    pad_width = k_width // 2
    padded_image = np.pad(image, ((pad_height, pad_height), (pad_width, pad_width)), mode='edge')
    
    # Create a view of the padded image with sliding windows
    windows = as_strided(padded_image,
                         shape=(i_height, i_width, k_height, k_width),
                         strides=padded_image.strides + padded_image.strides)
    
    # Perform the convolution
    return np.einsum('ijkl,kl->ij', windows, kernel)


if __name__ == "__main__":

    mf_mixed.f2py_setup()
    mf_mixed.f2py_compile('filters', ['filters.f90'])

    from filters import *   # Import the Fortran module

    # Load the image in grayscale mode

    print("Loading image...")
    image = cv2.imread('fortran_python.png', cv2.IMREAD_GRAYSCALE)
    print(image.dtype)

    print("Creating fortran array...")
    image_f = np.zeros_like(image, order='F', dtype=float)
    image_f[:] = image

    # Define the kernel size for the mean filter

    kernel_size = 7

    # Apply the mean filter to the image

    print("Applying mean filter (python)...")

    t0 = time.time()
    filtered_image1 = blur_filter_vectorized(image_f, kernel_size)
    t1 = time.time()

    print("Time (python): ", t1 - t0)

    print("Applying mean filter (fortran)...")
    filtered_image2 = np.zeros_like(image_f, order='F', dtype=float)

    n_samples = 100

    t0 = time.time()
    for i in range(n_samples):
        filters.mean_filter(image_f, kernel_size, filtered_image2)
    t1 = time.time()

    print("Time (fortran): ", (t1 - t0) / n_samples)

    print("Applying mean filter (cv2)...")

    t0 = time.time()
    for i in range(1):
        filtered_image3 = cv2.blur(image_f, (kernel_size, kernel_size))
    t1 = time.time()

    print("Time (python cv2): ", t1 - t0)

    plt.figure()
    plt.title('Python')
    plt.imshow(filtered_image1, cmap='gray')
    plt.figure()
    plt.title('Fortran')
    plt.imshow(filtered_image2, cmap='gray')
    plt.figure()
    plt.title('OpenCV')
    plt.imshow(filtered_image3, cmap='gray')
    plt.show()

    # Display the original and filtered images
    #cv2.imshow('Original Image', image)
    #cv2.imshow('Mean Filtered Image', filtered_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()