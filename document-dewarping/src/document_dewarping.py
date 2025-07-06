"""
Document Dewarping Tool with Fixed Image Display
"""

import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter1d
from PIL import Image, ImageTk
import customtkinter as ctk
import os

def preprocess_image(img):
    """Enhance image quality and convert to binary"""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(img)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def find_text_lines(binary_img):
    """Find text lines with improved peak detection"""
    h_proj = np.sum(binary_img == 0, axis=1)
    h_proj_smooth = gaussian_filter1d(h_proj, sigma=2)
    
    peaks = []
    window = 80  # Adjusted window size
    min_peak_height = np.mean(h_proj_smooth) * 0.5  # Adaptive threshold
    
    for i in range(window, len(h_proj_smooth) - window):
        if (h_proj_smooth[i] > h_proj_smooth[i-window:i].max() and
            h_proj_smooth[i] > h_proj_smooth[i+1:i+window].max() and
            h_proj_smooth[i] > min_peak_height):
            if not peaks or abs(i - peaks[-1]) > window:
                peaks.append(i)
    
    return peaks

def extract_line_points(binary_img, center_y, window_height=50):
    """Extract points along a text line"""
    height, width = binary_img.shape
    points = []
    window_width = 10
    step = 2
    
    for x in range(0, width - window_width, step):
        y_start = max(0, center_y - window_height)
        y_end = min(height, center_y + window_height)
        strip = binary_img[y_start:y_end, x:x+window_width]
        
        black_pixels = np.where(strip == 0)
        if len(black_pixels[0]) > window_width:
            y_positions = black_pixels[0]
            weights = np.exp(-0.5 * ((y_positions - len(y_positions)/2) / (len(y_positions)/4))**2)
            y = y_start + np.average(y_positions, weights=weights)
            points.append((x + window_width//2, y))
    
    return np.array(points)

def fit_curve(points):
    """Fit smooth curve through points"""
    if len(points) < 4:
        return None
    
    try:
        points = points[points[:, 0].argsort()]
        window = 5
        y_median = np.median(points[max(0, len(points)-window):len(points), 1])
        mask = np.abs(points[:, 1] - y_median) < 50
        points = points[mask]
        
        if len(points) < 4:
            return None
        
        f = interp1d(points[:, 0], points[:, 1], 
                    kind='cubic',
                    fill_value='extrapolate')
        
        y_pred = f(points[:, 0])
        if np.any(np.abs(y_pred - points[:, 1]) > 100):
            return None
            
        return f
    except:
        return None

def dewarp_line(binary_img, curve_func, center_y, window_height=50):
    """Dewarp a single text line"""
    height, width = binary_img.shape
    dewarped = np.ones((2 * window_height, width), dtype=np.uint8) * 255
    
    x_coords = np.arange(width)
    try:
        y_coords = curve_func(x_coords)
        y_coords = np.clip(y_coords, window_height, height - window_height)
        y_coords = gaussian_filter1d(y_coords, sigma=2.0)
        
        for x, src_y in zip(x_coords, y_coords):
            src_y = int(src_y)
            local_window = window_height
            y_start = max(0, src_y - local_window)
            y_end = min(height, src_y + local_window)
            strip = binary_img[y_start:y_end, x]
            dst_start = max(0, min(2 * window_height, window_height - (src_y - y_start)))
            dst_end = min(2 * window_height, dst_start + (y_end - y_start))
            if len(strip) > 0:
                dewarped[dst_start:dst_end, x] = strip[:dst_end-dst_start]
                
    except Exception as e:
        print(f"Error in dewarping: {str(e)}")
    
    return dewarped

def dewarp_page(binary_img):
    """Dewarp entire page"""
    line_positions = find_text_lines(binary_img)
    dewarped_lines = []
    line_viz = cv2.cvtColor(binary_img.copy(), cv2.COLOR_GRAY2BGR)
    padding = 20
    
    for y_pos in line_positions:
        points = extract_line_points(binary_img, y_pos)
        if len(points) < 4:
            continue
            
        curve_func = fit_curve(points)
        if curve_func is None:
            continue
            
        x_coords = np.arange(0, binary_img.shape[1], 5)
        y_coords = curve_func(x_coords)
        points = np.column_stack((x_coords, y_coords)).astype(np.int32)
        cv2.polylines(line_viz, [points], False, (0, 255, 0), 2)
        
        dewarped_line = dewarp_line(binary_img, curve_func, y_pos)
        padded_line = np.ones((dewarped_line.shape[0] + padding, dewarped_line.shape[1]), dtype=np.uint8) * 255
        padded_line[:-padding] = dewarped_line
        dewarped_lines.append(padded_line)
    
    if dewarped_lines:
        total_height = sum(line.shape[0] for line in dewarped_lines)
        result = np.ones((total_height, binary_img.shape[1]), dtype=np.uint8) * 255
        
        y_offset = 0
        for line in dewarped_lines:
            h = line.shape[0]
            result[y_offset:y_offset+h] = line
            y_offset += h
            
        return result, line_viz
    
    return binary_img.copy(), line_viz

def process_page_with_debug(image_path):
    """Process page and show intermediate results"""
    try:
        # Read image
        original = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if original is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        # Preprocess
        binary = preprocess_image(original)
        
        # Dewarp
        dewarped, lines_viz = dewarp_page(binary)
        
        # Create debug images
        debug_images = {
            '1. Original': original,
            '2. Binary': binary,
            '3. Detected Lines': lines_viz,
            '4. Final Dewarped': dewarped
        }
        
        return debug_images
    except Exception as e:
        print(f"Error processing page: {str(e)}")
        return None

class ImageDisplay(ttk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent)
        
        # Create frame with title
        self.frame = ttk.LabelFrame(self, text=title, padding=10)
        self.frame.pack(fill="both", expand=True)
        
        # Create canvas with scrollbars
        self.canvas = tk.Canvas(self.frame, bd=0, highlightthickness=0)
        self.h_scroll = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.v_scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        
        # Configure canvas scrolling
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        
        # Grid layout for scrollable canvas
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        # Initialize variables
        self.image = None
        self.photo = None
        self.display_size = (400, 400)
        self.zoom = 1.0

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def display_image(self, img):
        if img is None:
            return
            
        # Convert to RGB if needed
        if len(img.shape) == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        self.image = Image.fromarray(img_rgb)
        
        # Calculate size maintaining aspect ratio
        width, height = self.image.size
        aspect_ratio = width / height
        
        if width > height:
            new_width = min(width, self.display_size[0])
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, self.display_size[1])
            new_width = int(new_height * aspect_ratio)
        
        # Resize image
        resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create PhotoImage and display
        self.photo = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class DewarpingGUI:
    def __init__(self):
        # Create the main window
        self.root = ctk.CTk()
        self.root.title("Document Dewarping Tool")
        self.root.geometry("1200x800")
        
        # Configure grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create frames
        self.create_toolbar()
        self.create_image_grid()
        self.create_status_bar()
        
        # Initialize variables
        self.image_path = None
        self.debug_images = None

    def create_toolbar(self):
        # Create toolbar frame
        toolbar = ctk.CTkFrame(self.root)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Create buttons
        self.select_btn = ctk.CTkButton(
            toolbar, 
            text="Select Image",
            command=self.select_image,
            width=120
        )
        self.select_btn.pack(side="left", padx=5)
        
        self.process_btn = ctk.CTkButton(
            toolbar,
            text="Process Image",
            command=self.process_image,
            width=120,
            state="disabled"
        )
        self.process_btn.pack(side="left", padx=5)
        
        self.save_btn = ctk.CTkButton(
            toolbar,
            text="Save Result",
            command=self.save_result,
            width=120,
            state="disabled"
        )
        self.save_btn.pack(side="left", padx=5)

    def create_image_grid(self):
        # Create main display frame
        self.display_frame = ctk.CTkFrame(self.root)
        self.display_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Configure grid
        self.display_frame.grid_rowconfigure((0, 1), weight=1)
        self.display_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Create image displays
        self.displays = {
            'Original': ImageDisplay(self.display_frame, "Original Image"),
            'Binary': ImageDisplay(self.display_frame, "Binary Image"),
            'Detected Lines': ImageDisplay(self.display_frame, "Detected Lines"),
            'Final Dewarped': ImageDisplay(self.display_frame, "Final Dewarped")
        }
        
        # Position displays
        self.displays['Original'].grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.displays['Binary'].grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.displays['Detected Lines'].grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.displays['Final Dewarped'].grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def create_status_bar(self):
        # Create status bar
        self.status_bar = ctk.CTkFrame(self.root)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        self.status_label = ctk.CTkLabel(self.status_bar, text="Ready")
        self.status_label.pack(side="left", padx=5)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        
        if self.image_path:
            try:
                # Read and display original image
                img = cv2.imread(self.image_path)
                if img is not None:
                    self.displays['Original'].display_image(img)
                    self.process_btn.configure(state="normal")
                    self.status_label.configure(text=f"Loaded: {os.path.basename(self.image_path)}")
                else:
                    raise ValueError("Failed to load image")
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")

    def process_image(self):
        if self.image_path:
            try:
                self.status_label.configure(text="Processing...")
                self.root.update()
                
                # Process image
                debug_images = process_page_with_debug(self.image_path)
                
                if debug_images:
                    # Display all images
                    for title, img in debug_images.items():
                        display_title = title.split('. ')[1]
                        self.displays[display_title].display_image(img)
                    
                    self.save_btn.configure(state="normal")
                    self.status_label.configure(text="Processing complete")
                    self.debug_images = debug_images
                else:
                    self.status_label.configure(text="Processing failed")
            
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")

    def save_result(self):
        if self.debug_images and '4. Final Dewarped' in self.debug_images:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
            )
            
            if save_path:
                try:
                    cv2.imwrite(save_path, self.debug_images['4. Final Dewarped'])
                    self.status_label.configure(text=f"Saved: {os.path.basename(save_path)}")
                except Exception as e:
                    self.status_label.configure(text=f"Save error: {str(e)}")

    def run(self):
        self.root.mainloop()

def main():
    app = DewarpingGUI()
    app.run()

if __name__ == "__main__":
    main()