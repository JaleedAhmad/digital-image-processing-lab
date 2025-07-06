# Noise Estimation

This project estimates and removes various noise types (Salt & Pepper, Gaussian, Uniform, Rayleigh, Exponential) from grayscale images using MATLAB, focusing on chessboard patterns.

## Overview
The workflow includes generating noisy images, estimating noise type via statistical analysis, and applying tailored denoising filters.

## Getting Started

### Prerequisites
- MATLAB with Image Processing Toolbox.

### Installation
1. Ensure MATLAB is installed and configured.
2. Place the folder in your MATLAB working directory.

## Usage
1. Run `src/main.m` to test noise estimation on sample images.
2. Generated noisy images are in `noisy_images/`.
3. Denoised results are saved in `denoised_images/`.

## Files
- `src/main.m`: Test script.
- `src/estimate_noise.m`: Noise estimation function.
- `src/remove_noise.m`: Denoising function.
- `src/NoiseGeneration.m`: Noise generation script.
- `sample_images/`: Input placeholders.
- `outputs/`: Processed results.

## Notes
- Adjust noise parameters (e.g., variance, density) in `NoiseGeneration.m`.
- Check debug output in the MATLAB console for estimation details.

## License
[MIT License](https://github.com/your-username/image-processing-lab/blob/main/LICENSE).