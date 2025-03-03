import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def visualize_intensity(image_path):
    # Load image
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # Check image size and dimensions
    print(f"Image size: {pixels.shape}")
    print(f"Number of image dimensions: {len(pixels.shape)}")
    
    # Visualize grayscale image intensity
    plt.figure(figsize=(10, 8))
    
    # Display intensity map
    im = plt.imshow(pixels, cmap='hot')
    plt.title('Grayscale Intensity')
    
    # Add colorbar
    plt.colorbar(im, label='Intensity')
    
    # Add axis labels
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    
    plt.tight_layout()
    plt.show()

    # Print statistical information
    print("\nImage statistics:")
    print(f"Minimum value: {np.min(pixels)}")
    print(f"Maximum value: {np.max(pixels)}")
    print(f"Mean value: {np.mean(pixels):.2f}")
    print(f"Standard deviation: {np.std(pixels):.2f}")

    # Pixel value distribution histogram
    plt.figure(figsize=(10, 6))
    plt.hist(pixels.flatten(), bins=256, range=(0, 255), density=True)
    plt.title('Pixel Intensity Distribution')
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    image_path = 'korea_data.png'  # Path to the image for analysis
    visualize_intensity(image_path)