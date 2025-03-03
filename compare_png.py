import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats
import os

def load_and_process_image(image_path, target_size=(512, 512)):
    """
    Load and preprocess an image
    - Forcibly convert to RGB 3 channels
    - Resize to specified size
    - Apply Min-Max normalization
    """
    img = Image.open(image_path)
    
    # Forcibly convert to RGB (also convert grayscale images to 3 channels)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to target size
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(img).astype(float)
    
    # Normalize each channel
    normalized_array = np.zeros_like(img_array)
    for channel in range(3):
        channel_data = img_array[:,:,channel]
        if channel_data.max() != channel_data.min():  # Prevent division by zero
            normalized_array[:,:,channel] = (channel_data - channel_data.min()) * 255 / (channel_data.max() - channel_data.min())
        else:
            normalized_array[:,:,channel] = channel_data
    
    print(f"Loaded image shape from {image_path}: {normalized_array.shape}")
    print(f"Value range: [{normalized_array.min():.1f}, {normalized_array.max():.1f}]")
    
    return normalized_array.astype(np.uint8)

def calculate_pixel_statistics(img1_array, img2_array):
    """
    Calculate pixel-by-pixel statistics between two images
    """
    # Normalize image values to 0-1 range
    img1_norm = img1_array.astype(float) / 255.0
    img2_norm = img2_array.astype(float) / 255.0
    
    # Basic statistics
    diff = img1_norm - img2_norm
    mae = np.mean(np.abs(diff))
    mse = np.mean(diff ** 2)
    rmse = np.sqrt(mse)
    
    # Channel-wise correlation coefficients
    correlations = []
    for channel in range(3):  # RGB
        correlation = np.corrcoef(
            img1_norm[:,:,channel].flatten(),
            img2_norm[:,:,channel].flatten()
        )[0,1]
        correlations.append(correlation)
    
    # Channel-wise KL Divergence
    kl_divergences = []
    for channel in range(3):
        # Calculate histogram (0-1 range)
        hist1, _ = np.histogram(img1_norm[:,:,channel].flatten(), bins=50, range=(0,1), density=True)
        hist2, _ = np.histogram(img2_norm[:,:,channel].flatten(), bins=50, range=(0,1), density=True)
        
        # Add small value to prevent division by zero
        hist1 = hist1 + 1e-10
        hist2 = hist2 + 1e-10
        
        # KL Divergence 계산
        kl_div = np.sum(hist1 * np.log(hist1 / hist2))
        kl_divergences.append(kl_div)
    
    # Analyze distribution of pixel value differences
    diff_threshold = 0.1  # Consider pixels with >10% difference as significant
    significant_diff_ratio = np.mean(np.abs(diff) > diff_threshold)
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'Correlations_RGB': correlations,
        'KL_Divergences_RGB': kl_divergences,
        'Significant_Difference_Ratio': significant_diff_ratio
    }

def plot_comparison(img1_array, img2_array, statistics, save_path=None):
    """
    Visualize the comparison of two images
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Display original images
    axes[0,0].imshow(img1_array)
    axes[0,0].set_title('NowcastNet Image')
    axes[0,0].axis('off')
    
    axes[0,1].imshow(img2_array)
    axes[0,1].set_title('Converted USA Data')
    axes[0,1].axis('off')
    
    # Visualize difference (using normalized values)
    diff_img = np.abs(img1_array.astype(float) - img2_array.astype(float)) / 255.0
    diff_mean = np.mean(diff_img, axis=2)  # Average difference of RGB channels
    im = axes[0,2].imshow(diff_mean, cmap='hot')
    axes[0,2].set_title('Average Absolute Difference')
    axes[0,2].axis('off')
    plt.colorbar(im, ax=axes[0,2])
    
    # RGB 채널별 히스토그램 비교
    channel_names = ['Red', 'Green', 'Blue']
    for i in range(3):
        axes[1,i].hist(img1_array[:,:,i].flatten(), bins=50, alpha=0.5, density=True, label='NowcastNet', color='blue')
        axes[1,i].hist(img2_array[:,:,i].flatten(), bins=50, alpha=0.5, density=True, label='USA Data', color='red')
        axes[1,i].set_title(f'{channel_names[i]} Channel Distribution')
        axes[1,i].legend()
    
    # Compare histograms for each RGB channel
    stats_text = (
        f"MAE: {statistics['MAE']:.4f}\n"
        f"RMSE: {statistics['RMSE']:.4f}\n\n"
        f"Channel Correlations:\n"
        f"R: {statistics['Correlations_RGB'][0]:.4f}\n"
        f"G: {statistics['Correlations_RGB'][1]:.4f}\n"
        f"B: {statistics['Correlations_RGB'][2]:.4f}\n\n"
        f"Significant Difference Ratio: {statistics['Significant_Difference_Ratio']:.4f}"
    )
    plt.figtext(0.02, 0.02, stats_text, fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()

def analyze_image_pair(nowcast_path='processed_data.png', usa_path='usa_data.png', target_size=(512, 512), output_dir='comparison_results'):
    """
    Compare two images and save the results
    """
    # Create result directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load and preprocess images
    print(f"Processing images to size {target_size}...")
    nowcast_img = load_and_process_image(nowcast_path, target_size)
    usa_img = load_and_process_image(usa_path, target_size)
    
    print(f"Processed image shapes:")
    print(f"NowcastNet image: {nowcast_img.shape}")
    print(f"USA image: {usa_img.shape}")
    
    # Calculate statistics
    print("Calculating statistics...")
    stats = calculate_pixel_statistics(nowcast_img, usa_img)
    
    # Visualize and save results
    plot_comparison(
        nowcast_img, 
        usa_img, 
        stats,
        save_path=os.path.join(output_dir, 'image_comparison.png')
    )
    
    # Save statistics to text file
    with open(os.path.join(output_dir, 'statistics.txt'), 'w') as f:
        f.write(f"Image Comparison Statistics\n")
        f.write(f"='='='='='='='='='='='='='=\n")
        f.write(f"Original Size (NowcastNet): {Image.open(nowcast_path).size}\n")
        f.write(f"Original Size (USA Data): {Image.open(usa_path).size}\n")
        f.write(f"Processed Size: {target_size}\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    return stats

# Main execution code
if __name__ == "__main__":
    nowcast_path = 'processed_data.png'
    usa_path = 'korea_data.png'
    
    print(f"Analyzing images:")
    print(f"NowcastNet image: {nowcast_path}")
    print(f"USA data image: {usa_path}")
    
    stats = analyze_image_pair(nowcast_path, usa_path)
    
    print("\nAnalysis complete! Results saved in 'comparison_results' directory.")