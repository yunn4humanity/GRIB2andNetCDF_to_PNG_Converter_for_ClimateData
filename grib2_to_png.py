import pygrib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# grib2 파일 열기
grbs = pygrib.open('usa_data.grib2')
grb = grbs[1]

# 데이터와 위경도 가져오기
data, lats, lons = grb.data()

# 그림 설정 - 여백 제거
plt.figure(figsize=(8, 8))
ax = plt.gca()
ax.set_axis_off()

# 여백 제거
plt.margins(0,0)
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

# 데이터 시각화 - 흑백 컬러맵으로 변경
plt.pcolormesh(lons, lats, data, 
               cmap='Greys_r',     # Greys_r를 사용하여 반전된 흑백으로 표시
               norm=LogNorm(vmin=0.1, vmax=data.max()),
               )

# 불필요한 여백 제거
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())

# PNG로 저장 - facecolor를 검은색으로 설정
plt.savefig('usa_data.png', 
            bbox_inches='tight', 
            pad_inches=0, 
            dpi=300,
            facecolor='black',  # 배경색을 검은색으로 설정
            edgecolor='none')
plt.close()