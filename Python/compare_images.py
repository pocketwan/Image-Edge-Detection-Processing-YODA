import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

def compare_images(img1_path, img2_path, save_prefix='comparison'):
    # Load grayscale images
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        raise FileNotFoundError("One or both image paths are invalid or the files do not exist.")

    if img1.shape != img2.shape:
        raise ValueError("Images must have the same dimensions")

    # Compute SSIM
    ssim_score, diff_map = ssim(img1, img2, full=True)
    diff_map = (diff_map * 255).astype("uint8")

    # Compute PSNR
    psnr_score = cv2.PSNR(img1, img2)

    # Normalize PSNR into a similarity percentage (rough scale)
    psnr_percent = min(psnr_score / 100, 1.0) * 100
    ssim_percent = ssim_score * 100

    # Absolute Difference
    abs_diff = cv2.absdiff(img1, img2)

    # Plot results
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes[0, 0].imshow(img1, cmap='gray')
    axes[0, 0].set_title("ModelSim Output")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(img2, cmap='gray')
    axes[0, 1].set_title("Python Output")
    axes[0, 1].axis('off')

    axes[1, 0].imshow(abs_diff, cmap='hot')
    axes[1, 0].set_title("Absolute Difference")
    axes[1, 0].axis('off')

    axes[1, 1].bar(["SSIM", "PSNR"], [ssim_percent, psnr_percent], color=["green", "blue"])
    axes[1, 1].set_ylim(0, 100)
    axes[1, 1].set_ylabel("Similarity (%)")
    axes[1, 1].set_title("Similarity Metrics")

    plt.tight_layout()
    plt.savefig(f"{save_prefix}_visual_comparison.png")
    plt.show()

    print(f"SSIM Similarity: {ssim_percent:.2f}%")
    print(f"PSNR Similarity: {psnr_percent:.2f}%")
    return ssim_percent, psnr_percent


compare_images('man_clean_hdl.png', 'man_clean_python.png', save_prefix='man_comparison')
