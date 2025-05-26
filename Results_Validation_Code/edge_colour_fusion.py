import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys 

def edge_color_fusion(original_path, edge_path, output_path="fused.png"):
    """
    Fuses original color image with grayscale edges.
    
    Args:
        original_path: Path to original RGB image (e.g., 'input.png')
        edge_path: Path to grayscale edge map (e.g., 'edges.png')
        output_path: Output file name (default: 'fused.png')
    """
    # Load images
    original = np.array(Image.open(original_path).convert('RGB'))
    edges = np.array(Image.open(edge_path).convert('L'))  # Force grayscale
    
    # Resize edges to match original (if needed)
    if original.shape[:2] != edges.shape:
        edges = np.array(Image.fromarray(edges).resize((original.shape[1], original.shape[0])))
    
    # Normalize edge mask (0=strong edge, 1=no edge)
    edge_mask = 1.0 - (edges / 255.0)
    
    # Apply mask to each RGB channel
    fused = np.zeros_like(original)
    for c in range(3):  # R, G, B channels
        fused[:, :, c] = original[:, :, c] * edge_mask
    
    # Convert to 8-bit and save
    fused = np.clip(fused, 0, 255).astype(np.uint8)
    Image.fromarray(fused).save(output_path)
    print(f"Saved fused image to {output_path}")
    
    # Display results
    plt.figure(figsize=(12, 4))
    plt.subplot(131); plt.imshow(original); plt.title("Original")
    plt.subplot(132); plt.imshow(edges, cmap='gray'); plt.title("Edges")
    plt.subplot(133); plt.imshow(fused); plt.title("Fused")
    plt.show()



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python edge_colour_fusion.py <original_path> <edge_path> [output_path]")
        sys.exit(1)

    original_path = sys.argv[1]
    edge_path = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "fused.png"

    edge_color_fusion(original_path, edge_path, output_path)
