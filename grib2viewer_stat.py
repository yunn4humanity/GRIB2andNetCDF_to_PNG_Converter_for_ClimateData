import pygrib
import numpy as np
import matplotlib.pyplot as plt

# grib2 파일 열기
grbs = pygrib.open('usa_data.grib2')
grb = grbs[1]
data, lats, lons = grb.data()

data_flat = data.flatten()
lower_bound = -1000
upper_bound = 1000

# 범위 내의 데이터만 선택
masked_data = data_flat[(data_flat >= lower_bound) & (data_flat <= upper_bound)]

# 데이터의 고유값 확인
unique_values = np.unique(masked_data)
print("고유값 개수:", len(unique_values))
print("고유값 목록 (처음 20개):")
print(unique_values[:20])

# 히스토그램 그리기 (bins 수를 늘리고 로그 스케일 적용)
plt.figure(figsize=(12, 6))

# 서브플롯 1: 일반 스케일
plt.subplot(1, 2, 1)
plt.hist(masked_data, bins=1000)  # bins 수를 1000개로 증가
plt.title("일반 스케일")
plt.xlabel("값")
plt.ylabel("빈도")

# 서브플롯 2: 로그 스케일
plt.subplot(1, 2, 2)
plt.hist(masked_data, bins=1000)
plt.yscale('log')  # y축을 로그 스케일로
plt.title("로그 스케일")
plt.xlabel("값")
plt.ylabel("빈도 (로그)")

plt.tight_layout()
plt.show()

# 상세 통계 출력
print("\n상세 통계:")
print(f"데이터 범위: {np.min(masked_data):.10f} ~ {np.max(masked_data):.10f}")
print(f"평균값: {np.mean(masked_data):.10f}")
print(f"중앙값: {np.median(masked_data):.10f}")
print(f"표준편차: {np.std(masked_data):.10f}")