# Color Segmentation

This project segments image regions by color using Python and OpenCV, employing HSV/RGB thresholding. It may include a GUI for interactive segmentation.

## Overview
The script isolates objects by color (e.g., blue, green, red) and counts them, useful for applications like object detection in colorful scenes.

## Getting Started

### Prerequisites
- Python 3.x
- OpenCV (`pip install opencv-python`)
- Optional: GUI libraries (e.g., Tkinter) if a GUI is implemented.

### Installation
1. Navigate to `color-segmentation/src/`.
2. Install dependencies using `pip install -r requirements.txt` (create this file with `opencv-python` if needed).

## Usage
1. Place an image in `sample_images/`.
2. Run the script: `python src/color_segmentation.py`.
3. View segmented results in `outputs/` and check the console for object counts.

## Files
- `src/color_segmentation.py`: Main Python script.
- `sample_images/`: Input images.
- `outputs/`: Segmented images.

## Notes
- Modify HSV ranges in the script for different color targets.
- A GUI (if included) allows real-time threshold adjustments.

## License
[MIT License](https://github.com/your-username/image-processing-lab/blob/main/LICENSE).