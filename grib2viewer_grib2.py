import pygrib

# GRIB 파일 열기
grbs = pygrib.open('usa_data.grib2')

# 모든 메시지 출력
for grb in grbs:
    print(grb)

# 특정 메시지 선택 및 데이터 읽기
grb = grbs.select()[0]  # 첫 번째 메시지
data = grb.values  # 데이터 값
lats, lons = grb.latlons()  # 위도/경도 격자

print(data)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 8))
plt.pcolormesh(lons, lats, data)
plt.colorbar(label='Reflectivity (dBZ)')
plt.title('MRMS Composite Reflectivity')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()