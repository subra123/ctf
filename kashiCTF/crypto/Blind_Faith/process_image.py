import cv2
import numpy as np

# Load the image
img = cv2.imread('challenge.png', cv2.IMREAD_GRAYSCALE)

if img is None:
    print("Could not load image.")
else:
    # Sharpening kernel
    kernel = np.array([[-1,-1,-1], 
                       [-1, 9,-1],
                       [-1,-1,-1]])
    sharpened = cv2.filter2D(img, -1, kernel)
    
    # Save the sharpened image
    cv2.imwrite('sharpened.png', sharpened)
    print("Sharpened image saved to sharpened.png")
    
    # Try different thresholds to see if text becomes visible
    _, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite('threshold1.png', thresh1)
    print("Thresholded image saved to threshold1.png")
    
    # Adaptive threshold
    thresh2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    cv2.imwrite('threshold2.png', thresh2)
    print("Adaptive thresholded image saved to threshold2.png")
