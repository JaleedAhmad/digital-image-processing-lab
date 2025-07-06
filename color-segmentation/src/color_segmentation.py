
import cv2
import numpy as np

def count_objects(segmented_image, color_name):
    print(f"\nProcessing {color_name} objects...")
    
    # Convert to grayscale
    gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY)
    print(f"Converted {color_name} image to grayscale")
    
    # Threshold to binary
    _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    print(f"Created binary image for {color_name}")
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Found {len(contours)} initial contours for {color_name}")
    
    # Filter small contours (noise)
    min_contour_area = 100  # Adjust this threshold as needed
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    print(f"After filtering small contours, found {len(valid_contours)} valid {color_name} objects")
    
    # Draw contours for visualization
    result = segmented_image.copy()
    cv2.drawContours(result, valid_contours, -1, (0, 255, 0), 2)
    
    return len(valid_contours), result, binary

print("Starting image processing...")
image = cv2.imread('ExamImgQ1.png')
print("Original image loaded")
cv2.imshow('1. Original Image', image)

print("\nConverting to HSV color space...")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Color ranges (same as before)
lower_colorgreen = np.array([35, 100, 50])
upper_colorgreen = np.array([80, 255, 255])
lower_coloryellow = np.array([17, 150, 100])
upper_coloryellow = np.array([30, 255, 255])
lower_colorblue = np.array([90, 150, 70])
upper_colorblue = np.array([140, 255, 255])
lower_colorred1 = np.array([0, 120, 100])
upper_colorred1 = np.array([5, 255, 255])
lower_colorred2 = np.array([160, 120, 100])
upper_colorred2 = np.array([179, 255, 255])
lower_colorredorange = np.array([5, 50, 80])
upper_colorredorange = np.array([16, 255, 255])

print("\nCreating color masks and segmenting images...")
# Blue
mask_blue = cv2.inRange(hsv, lower_colorblue, upper_colorblue)
segmented_image_blue = cv2.bitwise_and(image, image, mask=mask_blue)

# Yellow
mask_yellow = cv2.inRange(hsv, lower_coloryellow, upper_coloryellow)
segmented_image_yellow = cv2.bitwise_and(image, image, mask=mask_yellow)

# Red
mask_red1 = cv2.inRange(hsv, lower_colorred1, upper_colorred1)
mask_red2 = cv2.inRange(hsv, lower_colorred2, upper_colorred2)
mask_red = mask_red1 + mask_red2
segmented_image_red = cv2.bitwise_and(image, image, mask=mask_red)

# Green
mask1 = cv2.inRange(hsv, lower_colorgreen, upper_colorgreen)
segmented_image_green = cv2.bitwise_and(image, image, mask=mask1)

# Orange
mask_orange = cv2.inRange(hsv, lower_colorredorange, upper_colorredorange)
segmented_image_orange = cv2.bitwise_and(image, image, mask=mask_orange)

# Show segmentation results
full_seg = segmented_image_blue + segmented_image_green + segmented_image_red + segmented_image_yellow + segmented_image_orange
cv2.imshow('2. Full Segmentation', full_seg)
cv2.imshow('2a. Segmented Blue', segmented_image_blue)
cv2.imshow('2b. Segmented Green', segmented_image_green)
cv2.imshow('2c. Segmented Red', segmented_image_red)
cv2.imshow('2d. Segmented Yellow', segmented_image_yellow)
cv2.imshow('2e. Segmented Orange', segmented_image_orange)

print("\nPerforming erosion operations...")
kernel = np.ones((5,5), np.uint8)

# Perform erosion
eroded_orange = cv2.erode(segmented_image_orange, kernel, iterations=1)
eroded_red = cv2.erode(segmented_image_red, kernel, iterations=1)
eroded_yellow = cv2.erode(segmented_image_yellow, kernel, iterations=1)
eroded_green = cv2.erode(segmented_image_green, kernel, iterations=1)
eroded_blue = cv2.erode(segmented_image_blue, kernel, iterations=1)

# Show erosion results
full_eroded = eroded_orange + eroded_red + eroded_yellow + eroded_green + eroded_blue
cv2.imshow('3. Full Erosion', full_eroded)
cv2.imshow('3a. Eroded Blue', eroded_blue)
cv2.imshow('3b. Eroded Green', eroded_green)
cv2.imshow('3c. Eroded Red', eroded_red)
cv2.imshow('3d. Eroded Yellow', eroded_yellow)
cv2.imshow('3e. Eroded Orange', eroded_orange)

print("\nCounting objects and drawing contours...")
# Count objects for each color
orange_count, orange_contours, orange_binary = count_objects(eroded_orange, "orange")
red_count, red_contours, red_binary = count_objects(eroded_red, "red")
yellow_count, yellow_contours, yellow_binary = count_objects(eroded_yellow, "yellow")
green_count, green_contours, green_binary = count_objects(eroded_green, "green")
blue_count, blue_contours, blue_binary = count_objects(eroded_blue, "blue")

# Show contour results
full_contours = orange_contours + red_contours + yellow_contours + green_contours + blue_contours
cv2.imshow('4. Full Contours', full_contours)
cv2.imshow('4a. Blue Contours', blue_contours)
cv2.imshow('4b. Green Contours', green_contours)
cv2.imshow('4c. Red Contours', red_contours)
cv2.imshow('4d. Yellow Contours', yellow_contours)
cv2.imshow('4e. Orange Contours', orange_contours)


print("\nFinal Results:")
print("=" * 20)
print(f"Number of orange objects: {orange_count}")
print(f"Number of red objects: {red_count}")
print(f"Number of yellow objects: {yellow_count}")
print(f"Number of green objects: {green_count}")
print(f"Number of blue objects: {blue_count}")
print("-" * 20)
print(f"Total number of objects: {orange_count + red_count + yellow_count + green_count + blue_count}")
print("=" * 20)

print("\nDisplayed windows show:")
print("1. Original Image")
print("2. Segmentation Results (Full + Individual Colors)")
print("3. Erosion Results (Full + Individual Colors)")
print("4. Contour Results (Full + Individual Colors)")
print("5. Binary Results (Full + Individual Colors)")

cv2.waitKey(0)
cv2.destroyAllWindows()