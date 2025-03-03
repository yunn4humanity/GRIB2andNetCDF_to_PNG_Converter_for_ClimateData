import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def visualize_intensity(image_path):
    # 이미지 로드
    img = Image.open(image_path)
    pixels = np.array(img)
    
    # 이미지 크기와 차원 확인
    print(f"이미지 크기: {pixels.shape}")
    print(f"이미지 차원 수: {len(pixels.shape)}")
    
    # 흑백 이미지 강도 시각화
    plt.figure(figsize=(10, 8))
    
    # 강도 맵 표시
    im = plt.imshow(pixels, cmap='hot')
    plt.title('Grayscale Intensity')
    
    # 컬러바 추가
    plt.colorbar(im, label='Intensity')
    
    # 축 레이블 추가
    plt.xlabel('X coordinate')
    plt.ylabel('Y coordinate')
    
    plt.tight_layout()
    plt.show()

    # 통계 정보 출력
    print("\n이미지 통계:")
    print(f"최소값: {np.min(pixels)}")
    print(f"최대값: {np.max(pixels)}")
    print(f"평균값: {np.mean(pixels):.2f}")
    print(f"표준편차: {np.std(pixels):.2f}")

    # 픽셀값 분포 히스토그램
    plt.figure(figsize=(10, 6))
    plt.hist(pixels.flatten(), bins=256, range=(0, 255), density=True)
    plt.title('Pixel Intensity Distribution')
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    image_path = 'korea_data.png'  # 분석할 이미지 경로
    visualize_intensity(image_path)