import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

def calculate_psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    return float('inf') if mse == 0 else 20 * np.log10(255.0 / np.sqrt(mse))

def compare_images(python_path, hdl_path):
    # Verify files exist
    if not all(os.path.exists(p) for p in [python_path, hdl_path]):
        print("Error: One or both image files don't exist")
        return

    # Load images with verification
    py_img = cv2.imread(python_path, cv2.IMREAD_GRAYSCALE)
    hdl_img = cv2.imread(hdl_path, cv2.IMREAD_GRAYSCALE)
    
    if py_img is None or hdl_img is None:
        print("Error: Failed to load images. Check file formats.")
        return

    print(f"Python image shape: {py_img.shape}")
    print(f"HDL image shape: {hdl_img.shape}")

    # Resize if needed
    if py_img.shape != hdl_img.shape:
        print("Resizing HDL image to match Python dimensions...")
        hdl_img = cv2.resize(hdl_img, (py_img.shape[1], py_img.shape[0]))
    
    # Calculate metrics
    diff = cv2.absdiff(py_img, hdl_img)
    mse = np.mean(diff**2)
    psnr = calculate_psnr(py_img, hdl_img)
    
    # Visual comparison
    plt.figure(figsize=(15, 5))
    
    # Corrected plotting syntax
    plt.subplot(131)
    plt.imshow(py_img, cmap='gray')
    plt.title('Python Output')
    
    plt.subplot(132)
    plt.imshow(hdl_img, cmap='gray')
    plt.title('HDL Output')
    
    plt.subplot(133)
    plt.imshow(diff, cmap='hot')
    plt.title(f'Difference\nPSNR: {psnr:.2f} dB')
    
    plt.tight_layout()
    
    output_path = 'comparison.png'
    plt.savefig(output_path)
    print(f"Comparison saved to {output_path}")
    plt.close()
    
    print(f"\n=== Results ===")
    print(f"PSNR: {psnr:.2f} dB (higher is better)")
    print(f"MSE: {mse:.2f} (lower is better)")
    print("Note: PSNR=∞ means identical images")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare grayscale images from Python and HDL output.")
    parser.add_argument("python_img", help="Path to Python-processed grayscale image")
    parser.add_argument("hdl_img", help="Path to HDL output grayscale image")
    args = parser.parse_args()

    compare_images(args.python_img, args.hdl_img)
    input("Press Enter to exit...")
