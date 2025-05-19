#!/usr/bin/env python3
"""
FPGA Median Filter with Timing YODA Project
---------------------------------------------------------------------------
Processes a HEX file with a 3x3 median filter and outputs a filtered HEX and PNG image.

Usage:
    python median.py noisy.hex filtered.hex --png output.png
"""

import numpy as np
import argparse
from PIL import Image
from pathlib import Path
import sys
import time

# Fixed FPGA image size
IMG_SIZE = (256, 256)

def debug_image(img_array, name):
    """Print debug info about the image array"""
    print(f"\n{name} properties:")
    print(f"- Shape: {img_array.shape}")
    print(f"- Data type: {img_array.dtype}")
    print(f"- Min value: {np.min(img_array)}")
    print(f"- Max value: {np.max(img_array)}")
    print(f"- Unique values: {len(np.unique(img_array))}")

def load_hex(hex_file):
    """Load HEX file with enhanced validation"""
    try:
        print(f"\nLoading HEX file: {hex_file}")
        with open(hex_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            
        if len(lines) != IMG_SIZE[0] * IMG_SIZE[1]:
            raise ValueError(f"Expected {IMG_SIZE[0]*IMG_SIZE[1]} pixels, got {len(lines)}")

        pixels = []
        bad_lines = []
        for i, line in enumerate(lines, 1):
            try:
                val = int(line, 16)
                if not 0 <= val <= 255:
                    bad_lines.append((i, line, "Value out of range"))
                pixels.append(val)
            except ValueError:
                bad_lines.append((i, line, "Invalid HEX format"))

        if bad_lines:
            print("\nFound problematic HEX lines (first 5 shown):")
            for i, line, err in bad_lines[:5]:
                print(f"Line {i}: '{line}' - {err}")
            raise ValueError(f"{len(bad_lines)} invalid HEX lines detected")

        img_array = np.array(pixels, dtype=np.uint8).reshape(IMG_SIZE)
        debug_image(img_array, "Loaded image")
        return img_array
        
    except Exception as e:
        print(f"\nFatal HEX load error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def save_png(img_array, png_file):
    """Save image with PNG format"""
    try:
        print(f"\nAttempting to save PNG to {png_file}")
        debug_image(img_array, "Image to be saved")
        
        # Convert to PIL Image
        img = Image.fromarray(img_array, 'L')
        
        # Save image
        img.save(png_file, 'PNG', 
                 optimize=True,
                 bits=8,
                 compression=9)
        
        # Verify the saved file
        if not Path(png_file).exists():
            raise IOError("PNG file was not created")
            
        try:
            test_img = Image.open(png_file)
            test_img.verify()
            print(f"\nPNG saved successfully and verified")
            print(f"File size: {Path(png_file).stat().st_size} bytes")
        except Exception as verify_error:
            raise ValueError(f"PNG verification failed: {str(verify_error)}")
            
    except Exception as e:
        print(f"\nPNG save error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def original_median_filter(img_array):
    """Median filter implementation"""
    pad = 1  # For 3x3 kernel
    padded = np.pad(img_array, pad, mode='reflect')
    filtered = np.zeros_like(img_array)
    
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            window = padded[y:y+3, x:x+3].flatten()
            
            # Sorting logic: odd-even sort (sufficient for 9 elements)
            for _ in range(4):
                for i in range(0, len(window)-1, 2):
                    if window[i] > window[i+1]:
                        window[i], window[i+1] = window[i+1], window[i]
                for i in range(1, len(window)-1, 2):
                    if window[i] > window[i+1]:
                        window[i], window[i+1] = window[i+1], window[i]
            
            filtered[y,x] = window[4]
    
    debug_image(filtered, "Filtered image")
    return filtered

def main():
    parser = argparse.ArgumentParser(
        description="Process FPGA image with guaranteed valid PNG output",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_hex", help="Input HEX file path")
    parser.add_argument("output_hex", help="Output HEX file path")
    parser.add_argument("--png", required=True, help="Output PNG file path")
    args = parser.parse_args()

    try:
        # Step 1: Load with extensive validation
        noisy_img = load_hex(args.input_hex)

        # Step 2: Process with original filter + timing
        print("\nStarting median filtering...")
        start_time = time.perf_counter()
        filtered_img = original_median_filter(noisy_img)
        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        print(f"\n[TIME] Median filtering completed in {elapsed_ms:.3f} ms")

        # Step 3: Save HEX output
        with open(args.output_hex, 'w') as f:
            np.savetxt(f, filtered_img.flatten(), fmt='%02X')

        # Step 4: Save and verify PNG
        save_png(filtered_img, args.png)

        print("\nProcessing complete!")
        print(f"HEX output: {args.output_hex}")
        print(f"PNG output: {args.png}")

    except Exception as e:
        print(f"\nProcessing failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
