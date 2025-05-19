#!/usr/bin/env python3
"""
Image to HEX Converter for YODA Project
---------------------------------------
Converts images to 256x256 greyscale HEX format for FPGA memory initialization
with optional salt-and-pepper noise injection.

Usage:
    python img2HEX.py <input_image> <output_file.hex> [--noise <amount>]

Options:
    --noise <amount>  Add salt-and-pepper noise (0.0 to 1.0) [default: 0.0]
"""

import sys
import argparse
import random
from PIL import Image
import numpy as np

# Configuration
TARGET_SIZE = (256, 256)  # Fixed FPGA-compatible resolution
SUPPORTED_EXT = ('.jpg', '.jpeg', '.png', '.bmp')

def add_salt_pepper_noise(image_array, noise_amount):
    """Add salt-and-pepper noise to image array"""
    if noise_amount <= 0:
        return image_array
    
    noisy = np.copy(image_array)
    height, width = noisy.shape
    
    # Calculate number of noise pixels
    num_noise = int(noise_amount * height * width)
    
    # Add salt (white pixels)
    coords = [np.random.randint(0, i-1, num_noise) for i in noisy.shape]
    noisy[coords[0], coords[1]] = 255
    
    # Add pepper (black pixels)
    coords = [np.random.randint(0, i-1, num_noise) for i in noisy.shape]
    noisy[coords[0], coords[1]] = 0
    
    return noisy

def validate_inputs(input_path, output_path):
    """Check if files meet requirements"""
    if not input_path.lower().endswith(SUPPORTED_EXT):
        raise ValueError(f"Unsupported file format. Supported: {SUPPORTED_EXT}")
    if output_path.split('.')[-1].lower() != 'hex':
        raise ValueError("Output file must have .hex extension")

def convert_to_hex(input_path, output_path, noise_amount=0.0):
    """Core conversion function with optional noise"""
    try:
        # Load and process image (convert to greyscale)
        img = Image.open(input_path).convert('L').resize(TARGET_SIZE)
        img_array = np.array(img)
        
        # Add noise if specified
        if noise_amount > 0:
            img_array = add_salt_pepper_noise(img_array, noise_amount)
            print(f"Added salt-and-pepper noise ({noise_amount*100:.1f}%)")
        
        pixels = img_array.flatten()
        
        # Write HEX file
        with open(output_path, 'w') as f:
            for px in pixels:
                f.write(f"{px:02X}\n")
        
        return len(pixels)
    
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Image to HEX converter for FPGA")
    parser.add_argument('input_image', help="Input image file path")
    parser.add_argument('output_hex', help="Output HEX file path")
    parser.add_argument('--noise', type=float, default=0.0,
                      help="Amount of salt-and-pepper noise (0.0 to 1.0)")
    
    try:
        args = parser.parse_args()
        
        validate_inputs(args.input_image, args.output_hex)
        if args.noise < 0 or args.noise > 1:
            raise ValueError("Noise amount must be between 0.0 and 1.0")
        
        pixel_count = convert_to_hex(args.input_image, args.output_hex, args.noise)
        
        print(f"Successfully converted {args.input_image}")
        print(f"Output: {args.output_hex} ({TARGET_SIZE[0]}x{TARGET_SIZE[1]}, {pixel_count} pixels)")
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()