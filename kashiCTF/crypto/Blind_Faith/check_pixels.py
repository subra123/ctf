import cv2
import numpy as np

# Load the image
img = cv2.imread('challenge.png', cv2.IMREAD_UNCHANGED)

if img is None:
    print("Could not load image.")
else:
    print(f"Shape: {img.shape}")
    print(f"Data type: {img.dtype}")
    
    # Check for unique values
    unique_vals = np.unique(img)
    print(f"Number of unique values: {len(unique_vals)}")
    print(f"Min value: {np.min(img)}, Max value: {np.max(img)}")
    
    # If the image is blurred, check if it looks like it has been processed with a specific kernel
    # Actually, let's just look at some pixel values
    print("Top left corner (5x5):")
    print(img[:5, :5])
    
    # Check if there's any repeating pattern in rows or columns
    # (e.g., if it's a sequence of numbers)
