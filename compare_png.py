import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy import stats
import os

def load_and_process_image(image_path, target_size=(512, 512)):
    """
    이미지를 로드하고 전처리
    - 강제로 RGB 3채널로 변환
    - 지정된 크기로 리사이징
    - Min-Max 정규화 적용
    """
    img = Image.open(image_path)
    
    # 강제로 RGB로 변환 (흑백이미지도 3채널로 변환)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 타겟 크기로 리사이징
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # numpy 배열로 변환
    img_array = np.array(img).astype(float)
    
    # 각 채널별로 정규화 수행
    normalized_array = np.zeros_like(img_array)
    for channel in range(3):
        channel_data = img_array[:,:,channel]
        if channel_data.max() != channel_data.min():  # 0으로 나누기 방지
            normalized_array[:,:,channel] = (channel_data - channel_data.min()) * 255 / (channel_data.max() - channel_data.min())
        else:
            normalized_array[:,:,channel] = channel_data
    
    print(f"Loaded image shape from {image_path}: {normalized_array.shape}")
    print(f"Value range: [{normalized_array.min():.1f}, {normalized_array.max():.1f}]")
    
    return normalized_array.astype(np.uint8)

def calculate_pixel_statistics(img1_array, img2_array):
    """
    두 이미지 간의 픽셀별 통계 계산
    """
    # 이미지 값을 0-1 범위로 정규화
    img1_norm = img1_array.astype(float) / 255.0
    img2_norm = img2_array.astype(float) / 255.0
    
    # 기본 통계
    diff = img1_norm - img2_norm
    mae = np.mean(np.abs(diff))
    mse = np.mean(diff ** 2)
    rmse = np.sqrt(mse)
    
    # 채널별 상관계수
    correlations = []
    for channel in range(3):  # RGB
        correlation = np.corrcoef(
            img1_norm[:,:,channel].flatten(),
            img2_norm[:,:,channel].flatten()
        )[0,1]
        correlations.append(correlation)
    
    # 채널별 KL Divergence
    kl_divergences = []
    for channel in range(3):
        # 히스토그램 계산 (0-1 범위)
        hist1, _ = np.histogram(img1_norm[:,:,channel].flatten(), bins=50, range=(0,1), density=True)
        hist2, _ = np.histogram(img2_norm[:,:,channel].flatten(), bins=50, range=(0,1), density=True)
        
        # 0으로 나누는 것을 방지하기 위해 작은 값 추가
        hist1 = hist1 + 1e-10
        hist2 = hist2 + 1e-10
        
        # KL Divergence 계산
        kl_div = np.sum(hist1 * np.log(hist1 / hist2))
        kl_divergences.append(kl_div)
    
    # 픽셀 값 차이의 분포 분석
    diff_threshold = 0.1  # 10% 이상 차이나는 픽셀을 significant difference로 간주
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
    두 이미지의 비교 결과를 시각화
    """
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # 원본 이미지들 표시
    axes[0,0].imshow(img1_array)
    axes[0,0].set_title('NowcastNet Image')
    axes[0,0].axis('off')
    
    axes[0,1].imshow(img2_array)
    axes[0,1].set_title('Converted USA Data')
    axes[0,1].axis('off')
    
    # 차이 시각화 (정규화된 값으로)
    diff_img = np.abs(img1_array.astype(float) - img2_array.astype(float)) / 255.0
    diff_mean = np.mean(diff_img, axis=2)  # RGB 채널의 평균 차이
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
    
    # 통계 정보를 그래프 위에 표시
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
    두 이미지를 비교하고 결과를 저장
    """
    # 결과 저장 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    
    # 이미지 로드 및 전처리
    print(f"Processing images to size {target_size}...")
    nowcast_img = load_and_process_image(nowcast_path, target_size)
    usa_img = load_and_process_image(usa_path, target_size)
    
    print(f"Processed image shapes:")
    print(f"NowcastNet image: {nowcast_img.shape}")
    print(f"USA image: {usa_img.shape}")
    
    # 통계 계산
    print("Calculating statistics...")
    stats = calculate_pixel_statistics(nowcast_img, usa_img)
    
    # 결과 시각화 및 저장
    plot_comparison(
        nowcast_img, 
        usa_img, 
        stats,
        save_path=os.path.join(output_dir, 'image_comparison.png')
    )
    
    # 통계 결과를 텍스트 파일로 저장
    with open(os.path.join(output_dir, 'statistics.txt'), 'w') as f:
        f.write(f"Image Comparison Statistics\n")
        f.write(f"='='='='='='='='='='='='='=\n")
        f.write(f"Original Size (NowcastNet): {Image.open(nowcast_path).size}\n")
        f.write(f"Original Size (USA Data): {Image.open(usa_path).size}\n")
        f.write(f"Processed Size: {target_size}\n\n")
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
    
    return stats

# 메인 실행 코드
if __name__ == "__main__":
    nowcast_path = 'processed_data.png'
    usa_path = 'korea_data.png'
    
    print(f"Analyzing images:")
    print(f"NowcastNet image: {nowcast_path}")
    print(f"USA data image: {usa_path}")
    
    stats = analyze_image_pair(nowcast_path, usa_path)
    
    print("\nAnalysis complete! Results saved in 'comparison_results' directory.")