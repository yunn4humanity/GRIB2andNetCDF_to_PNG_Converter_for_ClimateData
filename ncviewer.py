import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# NC 파일 열기
ds = nc.Dataset('korea_data.nc', 'r')

# DBZH 변수의 실제 구조 확인
dbzh_var = ds.variables['DBZH']
print("DBZH 변수 차원:", dbzh_var.dimensions)
print("DBZH 변수 속성:", dbzh_var.ncattrs())

# 데이터 읽기
dbzh = dbzh_var[:]

# 누락된 값 처리
if hasattr(dbzh_var, '_FillValue'):
    fill_value = dbzh_var._FillValue
    dbzh = np.ma.masked_equal(dbzh, fill_value)

# 데이터 재구성 시도
# 데이터의 실제 구조에 맞게 reshape
try:
    # 예시: 시간 × 고도 × 거리로 가정
    reshaped_data = dbzh.reshape(-1, len(ds.variables['range'][:]))
    
    plt.figure(figsize=(12, 8))
    plt.pcolormesh(reshaped_data)
    plt.colorbar(label='DBZH (dBZ)')
    plt.title('레이더 반사도(DBZH) 분포')
    plt.show()
    
except ValueError as e:
    print("데이터 재구성 오류:", e)

# 변수의 상세 정보 출력
print("\n변수 정보:")
for var_name in ds.variables:
    var = ds.variables[var_name]
    print(f"{var_name}:")
    print(f"  차원: {var.dimensions}")
    print(f"  형태: {var.shape}")
    print(f"  속성: {var.ncattrs()}")

ds.close()