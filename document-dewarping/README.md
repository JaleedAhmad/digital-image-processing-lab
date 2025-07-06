# Document Dewarping

This project implements document dewarping to correct distortions (e.g., bends, warps) in scanned pages using Python and OpenCV. It may include a GUI for interactive use.

## Overview
The script detects contours and applies perspective transformation to straighten warped documents, improving readability and OCR accuracy.

## Getting Started

### Prerequisites
- Python 3.x
- OpenCV (`pip install opencv-python`)
- Optional: GUI libraries (e.g., Tkinter) if a GUI is implemented.

### Installation
1. Navigate to `document-dewarping/src/`.
2. Install dependencies using `pip install -r requirements.txt` (create this file with `opencv-python` if needed).

## Usage
1. Place a warped image in `sample_images/` (e.g., `sample_image.jpg`).
2. Run the script: `python src/document_dewarping.py`.
3. Check `outputs/` for the dewarped result.

## Files
- `src/document_dewarping.py`: Main Python script.
- `sample_images/`: Input images.
- `outputs/`: Processed images.

## Notes
- Adjust contour detection parameters in the script for different document types.
- A GUI (if included) allows manual selection of document regions.

## License
[MIT License](https://github.com/your-username/image-processing-lab/blob/main/LICENSE).