import cv2
import numpy as np

# Load the image
#img = cv2.imread('Cat.png')

# Convert to grayscale
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.imread('filtered_cat_BP.png')#, cv2.IMREAD_GRAYSCALE)
# Define Sobel kernels
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]], dtype=np.float32)

sobel_y = sobel_x.T  # Transpose for y-direction

# Apply convolution
grad_x = cv2.filter2D(gray.astype(np.float32), -1, sobel_x)
grad_y = cv2.filter2D(gray.astype(np.float32), -1, sobel_y)

# Compute gradient magnitude
gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)

# Normalize to 0-255 and convert to uint8
gradient_magnitude = cv2.normalize(gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX)
edge_image = gradient_magnitude.astype(np.uint8)

# Save the result
cv2.imwrite('FilteredCat_sobel_edge_output2.png', edge_image)

# Optional: show the image
cv2.imshow('Sobel Edge Detection', edge_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

