# Image-Edge-Detection-Processing-YODA

This repository contains the design, implementation, and benchmarking of a digital accelerator for image processing, specifically focusing on **median filtering** and **Sobel edge detection** using **Verilog HDL** for FPGA simulation. A Python reference model serves as the golden measure for validation.


## Overview

-  Input: 8-bit grayscale image (e.g., 256×256 or 549×319)
-  Processing Steps:
  1. **Median Filter** – Noise reduction using a 3x3 sliding window
  2. **Sobel Edge Detector** – Feature extraction via Gx & Gy gradients
-  Output: Edge-detected image in `.hex` and `.png` formats
-  Simulation: Performed using **Vivado** (FPGA simulation environment)
-  Validation: Compared against a Python+OpenCV "Golden Measure"

---

###  Features

- 3×3 Median Filter (HDL + Python) for salt-and-pepper noise removal.
- Sobel Edge Detection (OpenCV + Verilog) with gradient magnitude computation.
- Testbenches for both modules
- HEX file I/O support for simulation image streaming
- Performance benchmarking (clock cycles, simulation time)
- Python validation pipeline (SSIM, MSE, PSNR)

## Prerequisites
- Python 3.8+ (with opencv-python, numpy, Pillow)
- Verilog Simulator ( ModelSim, Vivado)
- FPGA Toolchain (e.g., Xilinx Vivado for synthesis)

## Learnings & Future Work

- HDL accelerators need normalization to match floating-point software outputs.
- Visual similarity does not guarantee numerical accuracy (MSE ≠ 0).
**Future work includes:**
- Integrating HLS for rapid prototyping
- Hardware deployment on FPGA board
- Real-time webcam demo

## Contributors
**Lithernba Baninzi**
**Thabo Pokothoane**
**Nompumelelo Mohala**
